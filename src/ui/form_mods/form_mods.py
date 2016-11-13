# coding=utf-8

from blinker_herald import signals

from src.easi.ops import confirm
from src.meta_repo.local_meta_repo import LocalMetaRepo
from src.meta_repo.meta_repo import MetaRepo
from src.mod.mod import Mod
from src.qt import QAbstractTableModel, QModelIndex, Qt, QVariant, QSortFilterProxyModel, QHeaderView, \
    QWidget, QColor
from src.sig import SIG_CREATE_NEW_MOD
from src.sig import SIG_LOCAL_MOD_CHANGED
from src.ui.base.qwidget import BaseQWidget
from src.ui.dialog_own_mod.dialog import ModDetailsDialog
from src.ui.skeletons.form_own_mod_table import Ui_Form
from src.ui.dialog_mod_files.dialog import ModFilesDialog
from src.threadpool.threadpool import ThreadPool
from src.sig import SigProgress


class OwnModModel(QAbstractTableModel):
    columns_map = ['name', 'author', 'category', 'version', 'dcs_version', 'status']

    def __init__(self, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.__data = []

    def refresh_data(self):
        self.beginResetModel()
        self.__data = []
        mods = set(LocalMetaRepo()[self.parent().combo_repo.currentText()].mods)
        count = 0
        if mods:
            SigProgress().show('Updating mods...', '')
        for mod in mods:
            SigProgress().set_progress_text('Reading mod: {}'.format(mod.meta.name))
            mod_meta = mod.meta
            values = list([str(mod_meta[attr]) for attr in self.columns_map])
            print(values)
            self.__data.append(
                (values, mod, mod.has_changed)
            )
            count += 1
            SigProgress().set_progress((count / len(mods)) * 100)
        self.endResetModel()

    def data(self, index: QModelIndex, role=Qt.DisplayRole):
        if not index.isValid():
            return QVariant()
        if role == Qt.DisplayRole:
            return self.__data[index.row()][0][index.column()]
        elif role == Qt.UserRole:
            return self.__data[index.row()][1]
        elif role == Qt.ForegroundRole:
            if self.__data[index.row()][2]:
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
            self.set_repo_labels()
            self.proxy.sort(0, Qt.AscendingOrder)
            self.refresh_data()

        SIG_LOCAL_MOD_CHANGED.connect(refresh_mod_list, weak=False)

        self.connect_signals()

        self.pool = ThreadPool(1, 'form_mods')

    @property
    def selected_meta_repo(self) -> MetaRepo:
        return LocalMetaRepo()[self.combo_repo.currentText()]

    def __refresh_data(self):
        self.btn_details.setEnabled(False)
        self.model.refresh_data()
        self.set_repo_labels()
        self.resize_columns()

    def refresh_data(self):
        self.pool.queue_task(self.__refresh_data)

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
        self.btn_create_mod.clicked.connect(self.create_new_mod)
        self.btn_details.clicked.connect(self.show_details_for_selected_mod)

    def delete_mod(self):
        if confirm(
                'Are you sure you want to delete you want to delete "{}"?\n\n'
                '(all files will be moved to the recycle bin)'.format(
                    self.selected_mod.meta.name)):
            self.table.setUpdatesEnabled(False)
            self.selected_meta_repo.trash_mod(self.selected_mod.meta.name)
            self.table.setUpdatesEnabled(True)

    def create_new_mod(self, _):
        SIG_CREATE_NEW_MOD.send(meta_repo_name=self.selected_meta_repo.name)
        self.resize_columns()

    @property
    def selected_mod(self) -> Mod:
        mod = self.table.selectedIndexes()[0].data(Qt.UserRole)
        if isinstance(mod, Mod):
            return mod
        return None

    def show_details_for_selected_mod(self):
        ModDetailsDialog.make(self.selected_mod, self.selected_meta_repo, self)
        self.resize_columns()

    def on_double_click(self, _):
        if self.selected_mod:
            ModFilesDialog(self.selected_mod, self).qobj.exec()
            # for x in self.selected_mod.local_files:
            #     print(x)
            # self.show_details_for_selected_mod()

    def on_click(self, _):
        if self.selected_mod:
            self.btn_details.setEnabled(True)

    def set_repo_labels(self):
        if self.selected_meta_repo.push_perm:
            self.label_push_perm.setText('yes')
            self.label_push_perm.setStyleSheet('QLabel { color : green; }')
        else:
            self.label_push_perm.setText('no')
            self.label_push_perm.setStyleSheet('QLabel { color : red; }')


class ModEditor(BaseQWidget):
    def __init__(self, parent=None):
        BaseQWidget.__init__(self, _OwnModsTable(parent))
