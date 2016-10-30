# coding=utf-8

from blinker_herald import signals

from src.mod.create_new_mod import create_new_mod
from src.mod.local_mod import LocalMod
from src.mod.mod_objects.mod_base import BaseMod
from src.qt import QAbstractTableModel, QModelIndex, Qt, QVariant, QSortFilterProxyModel, QHeaderView, \
    QWidget, QColor
from src.ui.base.qwidget import BaseQWidget
from src.ui.dialog_edit_mod.dialog import EditModDialog
from src.ui.dialog_mod_manager.single_mod_view import SingleModViewDialog
from src.ui.skeletons.form_own_mod_table import Ui_Form
from src.ui.dialog_confirm.dialog import ConfirmDialog


class OwnModModel(QAbstractTableModel):
    columns_map = ['name', 'category', 'version', 'dcs_version', 'status']

    def __init__(self, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.__data = []

    def refresh_data(self):
        self.beginResetModel()
        self.__data = [draft for draft in LocalMod.drafts()]
        self.endResetModel()

    def data(self, index: QModelIndex, role=Qt.DisplayRole):
        if not index.isValid():
            return QVariant()
        if role == Qt.DisplayRole:
            return getattr(self.__data[index.row()], self.columns_map[index.column()])
        elif role == Qt.UserRole:
            return self.__data[index.row()]
        elif role == Qt.ForegroundRole:
            if self.__data[index.row()].has_changed:
                return QColor(Qt.blue)
            else:
                return QColor(Qt.black)

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.__data)

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self.columns_map)

    def headerData(self, col, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(str(self.columns_map[col]).capitalize().replace('_', ' '))
        else:
            return super(OwnModModel, self).headerData(col, orientation, role)


class _OwnModsTable(Ui_Form, QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent, flags=Qt.Widget)
        self.setupUi(self)
        self.model = OwnModModel(self)
        self.proxy = QSortFilterProxyModel(self)
        self.proxy.setSourceModel(self.model)
        self.table.setModel(self.proxy)
        self.table.verticalHeader().hide()
        self.table.horizontalHeader().show()
        self.table.setSelectionMode(1)
        self.table.setSelectionBehavior(1)
        self.table.setSortingEnabled(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.btn_create_mod.clicked.connect(self.create_new_mod)
        self.btn_view_files.clicked.connect(self.view_files)

        # noinspection PyUnusedLocal
        def refresh_mod_list(sender, signal_emitter, *args, **kwargs):
            if sender == 'MainUi':
                self.model.refresh_data()
                self.table.resizeColumnsToContents()
                self.proxy.sort(0, Qt.AscendingOrder)

        # signals.post_cache_changed_event.connect(refresh_mod_list, weak=False)
        signals.post_show.connect(refresh_mod_list, weak=False)

        self.connect_signals()

    # noinspection PyUnresolvedReferences
    def connect_signals(self):
        self.table.doubleClicked.connect(self.on_double_click)
        self.btn_trash_mod.clicked.connect(self.delete_mod)

    def delete_mod(self):
        if ConfirmDialog.make('Are you sure you want to delete you want to trash {}?'.format(self.selected_mod.name)):
            self.table.setUpdatesEnabled(False)
            self.selected_mod.trash()
            self.model.refresh_data()
            self.table.setUpdatesEnabled(True)

    def create_new_mod(self, _):
        create_new_mod(self)
        self.model.refresh_data()
        self.proxy.sort(0, Qt.AscendingOrder)

    def view_files(self):
        SingleModViewDialog(self.selected_mod, self)

    @property
    def selected_mod(self) -> BaseMod:
        return self.table.selectedIndexes()[0].data(Qt.UserRole)

    def on_double_click(self, _):
        EditModDialog.make(self.selected_mod, self)

    def show(self):
        self.proxy.sort(0, Qt.AscendingOrder)


class OwnModsTable(BaseQWidget):
    def __init__(self, parent=None):
        BaseQWidget.__init__(self, _OwnModsTable(parent))
