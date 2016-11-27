# coding=utf-8

import webbrowser

from blinker_herald import signals

from src.easi.ops import confirm
from src.repo.local_meta_repo import LocalMetaRepo
from src.repo.meta_repo import MetaRepo
from src.qt import QAbstractTableModel, QModelIndex, Qt, QVariant, QSortFilterProxyModel, QHeaderView, \
    QWidget, QColor
from src.sig import SIG_LOCAL_REPO_CHANGED, SigMsg
from src.ui.base.qwidget import BaseQWidget
from src.easi.ops import simple_input
from src.ui.dialog_repo.dialog import RepoDetailsDialog
from src.ui.skeletons.form_repository_table import Ui_Form


class MetaRepoModel(QAbstractTableModel):
    columns_map = ['name', 'push_perm']

    def __init__(self, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.__data = []

    def refresh_data(self):
        self.beginResetModel()
        self.__data = [mod for mod in LocalMetaRepo().repos]
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
            return super(MetaRepoModel, self).headerData(col, orientation, role)


class _MetaRepoTable(Ui_Form, QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent, flags=Qt.Widget)
        self.setupUi(self)
        self.model = MetaRepoModel(self)
        self.proxy = QSortFilterProxyModel(self)
        self.proxy.setSourceModel(self.model)
        self.table.setModel(self.proxy)
        self.table.verticalHeader().hide()
        self.table.horizontalHeader().show()
        self.table.setSelectionMode(1)
        self.table.setSelectionBehavior(1)
        self.table.setSortingEnabled(True)

        # noinspection PyUnusedLocal
        @signals.post_show.connect_via('MainUi', weak=False)
        def refresh_mod_list(sender, *args, **kwargs):
            self.model.refresh_data()
            self.resize_columns()

        SIG_LOCAL_REPO_CHANGED.connect(refresh_mod_list, weak=False)
        self.proxy.sort(0, Qt.AscendingOrder)

        self.connect_signals()
        self.btn_remove.setEnabled(False)

    def showEvent(self, event):
        self.set_repo_btn(False)
        super(_MetaRepoTable, self).showEvent(event)

    def resize_columns(self):
        for x in range(len(self.model.columns_map)):
            self.table.horizontalHeader().setSectionResizeMode(x, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

    # noinspection PyUnresolvedReferences
    def connect_signals(self):
        self.table.doubleClicked.connect(self.on_double_click)
        self.table.clicked.connect(self.on_click)
        self.btn_add.clicked.connect(self.add_repository)
        self.btn_remove.clicked.connect(self.remove_repository)
        self.btn_open_on_gh.clicked.connect(self.show_on_github)
        self.btn_details.clicked.connect(self.show_details_for_selected_repo)

    def show_on_github(self):
        webbrowser.open_new_tab(self.selected_repo.github_url)

    def add_repository(self):
        self.table.setUpdatesEnabled(False)
        repo_owner = simple_input(
            title='Adding repository',
            parent=self
        )
        if repo_owner:
            try:
                LocalMetaRepo().add_repo(repo_owner)
            except FileNotFoundError:
                SigMsg().show('Error', 'The repository was not found')
        self.table.setUpdatesEnabled(True)

    def remove_repository(self):
        self.table.setUpdatesEnabled(False)
        if confirm(
                'Are you sure you want to remove this repository ?\n\n'
                '(the repository will be deleted the next time EASI starts)',
                'Removing: {}'.format(self.selected_repo.name)
        ):
            LocalMetaRepo().remove_repo(self.selected_repo.name)
        self.table.setUpdatesEnabled(True)

    @property
    def selected_repo(self) -> MetaRepo:
        return self.table.selectedIndexes()[0].data(Qt.UserRole)

    def show_details_for_selected_repo(self):
        RepoDetailsDialog(self.selected_repo, self).qobj.exec()
        self.resize_columns()

    def on_double_click(self, _):
        if isinstance(self.selected_repo, MetaRepo):
            self.show_details_for_selected_repo()

    def on_click(self, _):
        if isinstance(self.selected_repo, MetaRepo):
            if any(
                    {self.selected_repo is LocalMetaRepo().own_meta_repo,
                     self.selected_repo is LocalMetaRepo().root_meta_repo}
            ):
                self.btn_remove.setEnabled(False)
            else:
                self.btn_remove.setEnabled(True)
            self.set_repo_btn(True)

    def set_repo_btn(self, value: bool):
        self.btn_details.setEnabled(value)
        self.btn_open_on_gh.setEnabled(value)


class MetaRepoTable(BaseQWidget):
    def __init__(self, parent=None):
        BaseQWidget.__init__(self, _MetaRepoTable(parent))
