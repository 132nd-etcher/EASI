# coding=utf-8

import os

from blinker_herald import signals

from src.cache.cache_event import CacheEvent
from src.easi.ops import confirm, long_input
from src.git.wrapper import GitRepository
from src.low.custom_path import Path
from src.qt import QAbstractTableModel, QModelIndex, QVariant, QIcon, \
    qt_resources, QSortFilterProxyModel, QColor
from src.qt import Qt, QWidget
from src.ui.skeletons.form_git_files import Ui_Form


class GitFilesModel(QAbstractTableModel):
    def __init__(self, repo: GitRepository, parent):
        QAbstractTableModel.__init__(self, parent)
        self.__data = []
        self.repo = repo
        self.show_unchanged = False

    def refresh_data(self):
        self.beginResetModel()
        self.__data = []
        if self.repo is not None:
            assert isinstance(self.repo, GitRepository)
            changed = set()
            for x in self.repo.working_dir_new:
                self.__data.append(('new', x))
                changed.add(x)
            for x in self.repo.working_dir_modified:
                self.__data.append(('modified', x))
                changed.add(x)
            for x in self.repo.working_dir_deleted:
                self.__data.append(('deleted', x))
                changed.add(x)
            if self.show_unchanged:
                for root, dirs, files in os.walk(self.repo.path.abspath(), topdown=True):
                    dirs[:] = [d for d in dirs if d not in ['.git']]
                    if root == '.git':
                        continue
                    for file in files:
                        file_path = os.path.join(root, file)
                        rel_path = os.path.relpath(file_path, self.repo.path.abspath()).replace('\\', '/')
                        if rel_path not in changed:
                            self.__data.append(('unchanged', rel_path))
        self.endResetModel()

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.__data)

    def columnCount(self, parent=None, *args, **kwargs):
        return 2

    def data(self, index: QModelIndex, role=Qt.DisplayRole):
        if not index.isValid():
            return QVariant()
        if role == Qt.DisplayRole:
            return self.__data[index.row()][index.column()]
        if role == Qt.UserRole:
            return self.__data[index.row()]
        if role == Qt.ForegroundRole:
            if 'new' in self.__data[index.row()][0]:
                return QColor(Qt.darkGreen)
            if 'modified' in self.__data[index.row()][0]:
                return QColor(Qt.blue)
            if 'deleted' in self.__data[index.row()][0]:
                return QColor(Qt.red)
            return QColor(Qt.black)

    def headerData(self, column, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            if column == 0:
                return 'Status'
            elif column == 1:
                return 'File path'
        return super(GitFilesModel, self).headerData(column, orientation, role)


class GitFilesWidget(QWidget, Ui_Form):
    def __init__(self, repo: GitRepository, parent=None):
        QWidget.__init__(self, parent, flags=Qt.Widget)
        self.setupUi(self)
        self.setWindowIcon(QIcon(qt_resources.app_ico))
        self.__repo = repo
        self.model = GitFilesModel(self.repo, self)
        self.proxy = QSortFilterProxyModel(self)
        self.proxy.setSourceModel(self.model)
        self.table.setModel(self.proxy)
        self.table.verticalHeader().hide()
        self.table.setColumnWidth(0, 80)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(1)
        self.table.setSelectionMode(1)
        self.btn_open.clicked.connect(self.open_repo_folder)
        self.btn_accept.clicked.connect(self.commit_changes)
        self.btn_reset.clicked.connect(self.reset_changes)
        self.check_show_unchanged.clicked.connect(self.show_unchanged)
        # noinspection PyUnresolvedReferences
        self.model.modelReset.connect(self.on_model_reset)

        # noinspection PyUnusedLocal
        def cache_signal_handler(sender, signal_emitter, event: CacheEvent):
            if self.repo is None:
                return
            if str(event.src.abspath()).startswith(str(self.repo.path.abspath())):
                self.model.refresh_data()

        self.cache_signal_handler = cache_signal_handler
        self.table.doubleClicked.connect(self.on_double_click)
        self.table.clicked.connect(self.on_click)
        self.btn_changes.clicked.connect(self.show_changes)

    def on_click(self, _):
        if isinstance(self.selected_file, tuple):
            self.btn_changes.setEnabled(True)

    def show_changes(self):
        path = Path(self.repo.path.joinpath(self.selected_file[1]))
        self.repo.show_file_diff(path)

    def on_double_click(self, _):
        self.show_changes()

    @property
    def selected_file(self):
        return self.table.selectedIndexes()[0].data(Qt.UserRole)

    @property
    def repo(self):
        return self.__repo

    @repo.setter
    def repo(self, value):
        self.__repo = value
        self.model.repo = value

    def show_unchanged(self, value: bool):
        self.model.show_unchanged = value
        self.model.refresh_data()

    def on_model_reset(self):
        if self.repo is not None:
            self.set_global_buttons(len(self.repo.status) > 0)

    def set_global_buttons(self, value: bool):
        self.btn_accept.setEnabled(value)
        self.btn_reset.setEnabled(value)

    def commit_changes(self):
        if self.repo is not None:
            commit_msg = long_input(
                title='Describe your changes',
                text='Write a short summary of the changes you just made:',
                parent=self,
            )
            if commit_msg is None:
                return
            self.repo.commit(msg=commit_msg, add_all=True)
            self.repo.push()
            self.model.refresh_data()

    def reset_changes(self):
        if self.repo is None:
            return
        if confirm('WARNING: resetting this mod will revert all changes made since last commit.\n\n'
                   'This is a destructive operation, and you may loose some of your work.\n\n'
                   'Are you sure you want to continue?'):
            self.repo.hard_reset()
            for x in self.repo.working_dir_new:
                os.remove(os.path.join(self.repo.path.abspath(), x))

    def open_repo_folder(self):
        if self.repo is not None:
            os.startfile(self.repo.path.abspath())

    def showEvent(self, event):
        if self.repo is not None:
            self.setWindowTitle('Showing files for: {}'.format(self.repo.path.abspath()))
        signals.post_cache_changed_event.connect(self.cache_signal_handler, weak=False)
        self.model.refresh_data()
        self.btn_changes.setEnabled(False)
        super(GitFilesWidget, self).showEvent(event)

    def hideEvent(self, event):
        signals.post_cache_changed_event.disconnect(self.cache_signal_handler)
        super(GitFilesWidget, self).hideEvent(event)
