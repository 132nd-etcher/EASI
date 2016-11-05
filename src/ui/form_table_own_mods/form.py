# coding=utf-8

from blinker_herald import signals

from src.sig import SIG_LOCAL_MOD_CHANGED
from src.mod.mod import Mod
from src.qt import QAbstractTableModel, QModelIndex, Qt, QVariant, QSortFilterProxyModel, QHeaderView, \
    QWidget, QColor
from src.ui.base.qwidget import BaseQWidget
from src.ui.skeletons.form_own_mod_table import Ui_Form
from src.low import constants
from src.rem.gh.gh_session import GHSession
from src.ui.dialog_confirm.dialog import ConfirmDialog
from src.ui.dialog_gh_login.dialog import GHLoginDialog
from src.ui.dialog_own_mod.dialog import ModDetailsDialog
from src.meta_repo.local_meta_repo import LocalMetaRepo
from src.meta_repo.meta_repo import MetaRepo


class OwnModModel(QAbstractTableModel):
    columns_map = ['name', 'author', 'category', 'version', 'dcs_version', 'status']

    def __init__(self, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.__data = []

    def refresh_data(self):
        self.beginResetModel()
        self.__data = list(LocalMetaRepo()[self.parent().combo_repo.currentText()].mods)
        self.endResetModel()

    def data(self, index: QModelIndex, role=Qt.DisplayRole):
        if not index.isValid():
            return QVariant()
        if role == Qt.DisplayRole:
            return getattr(self.__data[index.row()].meta, self.columns_map[index.column()])
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
        self.btn_create_mod.clicked.connect(self.create_new_mod)
        self.btn_details.clicked.connect(self.show_details_for_selected_mod)
        self.btn_details.setEnabled(False)

        # noinspection PyUnusedLocal
        def refresh_mod_list(*args, **kwargs):
            self.refresh_data()

        # noinspection PyUnusedLocal
        @signals.post_show.connect_via('MainUi', weak=False)
        def on_ui_creation(*args, **kwargs):
            self.combo_repo.addItems([repo.name for repo in LocalMetaRepo().repos])
            if LocalMetaRepo().own_meta_repo:
                self.combo_repo.setCurrentText(LocalMetaRepo().own_meta_repo.name)
            self.proxy.sort(0, Qt.AscendingOrder)
            self.refresh_data()

        SIG_LOCAL_MOD_CHANGED.connect(refresh_mod_list, weak=False)

        self.connect_signals()

    @property
    def selected_meta_repo(self) -> MetaRepo:
        return LocalMetaRepo()[self.combo_repo.currentText()]

    def refresh_data(self):
        self.btn_details.setEnabled(False)
        self.model.refresh_data()
        self.resize_columns()

    def resize_columns(self):
        for x in range(len(self.model.columns_map)):
            self.table.horizontalHeader().setSectionResizeMode(x, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

    # noinspection PyUnresolvedReferences
    def connect_signals(self):
        self.table.doubleClicked.connect(self.on_double_click)
        self.btn_trash_mod.clicked.connect(self.delete_mod)
        self.table.clicked.connect(self.on_click)
        self.combo_repo.currentIndexChanged.connect(self.refresh_data)

    def delete_mod(self):
        if ConfirmDialog.make(
                'Are you sure you want to delete you want to delete "{}"?\n\n'
                '(all files will be moved to the recycle bin)'.format(
                    self.selected_mod.meta.name)):
            raise NotImplementedError('mod trash')
            # self.table.setUpdatesEnabled(False)
            # LocalMod().trash_mod(self.selected_mod.meta.name)
            # self.table.setUpdatesEnabled(True)

    def create_new_mod(self, _):
        if not GHSession().has_valid_token:
            if ConfirmDialog.make('Creating a mod requires a valid Github account.<br><br>'
                                  'Would you like to connect your Github account now?',
                                  'Github account not connected'):
                if not GHLoginDialog.make(constants.MAIN_UI):
                    return
            else:
                return
        ModDetailsDialog(None, self.selected_meta_repo, self).qobj.exec()
        self.resize_columns()

    @property
    def selected_mod(self) -> Mod:
        return self.table.selectedIndexes()[0].data(Qt.UserRole)

    def show_details_for_selected_mod(self):
        ModDetailsDialog(self.selected_mod, self.selected_meta_repo, self).qobj.exec()
        self.resize_columns()

    def on_double_click(self, _):
        if isinstance(self.selected_mod, Mod):
            self.show_details_for_selected_mod()

    def on_click(self, _):
        if isinstance(self.selected_mod, Mod):
            self.btn_details.setEnabled(True)


class ModEditor(BaseQWidget):
    def __init__(self, parent=None):
        BaseQWidget.__init__(self, _OwnModsTable(parent))
