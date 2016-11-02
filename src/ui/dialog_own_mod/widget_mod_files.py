# coding=utf-8

import os

from blinker_herald import signals

from src.cache.cache import CacheEvent
from src.qt import QAbstractTableModel, QDialog, dialog_default_flags, Qt, QModelIndex, QVariant, QIcon, \
    qt_resources, QSortFilterProxyModel, QColor
from src.ui.dialog_confirm.dialog import ConfirmDialog
from src.ui.dialog_long_input.dialog import LongInputDialog


from src.ui.skeletons.form_mod_files import Ui_Form
from src.qt import Qt, QWidget
from src.mod.mod import Mod


class ModFilesModel(QAbstractTableModel):
    def __init__(self, mod: Mod, parent):
        QAbstractTableModel.__init__(self, parent)
        self.__data = []
        self.mod = mod
        self.show_unchanged = False

    def refresh_data(self):
        self.beginResetModel()
        self.__data = []
        if self.mod is not None:
            assert isinstance(self.mod, Mod)
            changed = set()
            for x in self.mod.repo.working_dir_new:
                self.__data.append(('new', x))
                changed.add(x)
            for x in self.mod.repo.working_dir_modified:
                self.__data.append(('modified', x))
                changed.add(x)
            for x in self.mod.repo.working_dir_deleted:
                self.__data.append(('deleted', x))
                changed.add(x)
            if self.show_unchanged:
                for root, dirs, files in os.walk(self.mod.repo.path.abspath(), topdown=True):
                    dirs[:] = [d for d in dirs if d not in ['.git']]
                    if root == '.git':
                        continue
                    for file in files:
                        file_path = os.path.join(root, file)
                        rel_path = os.path.relpath(file_path, self.mod.repo.path.abspath()).replace('\\', '/')
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
        return super(ModFilesModel, self).headerData(column, orientation, role)


class ModFilesWidget(QWidget, Ui_Form):
    def __init__(self, mod: Mod or None, parent=None):
        QWidget.__init__(self, parent, flags=Qt.Widget)
        self.setupUi(self)
        self.setWindowIcon(QIcon(qt_resources.app_ico))
        self.__mod = mod
        self.model = ModFilesModel(self.mod, self)
        self.proxy = QSortFilterProxyModel(self)
        self.proxy.setSourceModel(self.model)
        self.table.setModel(self.proxy)
        # self.table.horizontalHeader().hide()
        self.table.verticalHeader().hide()
        self.table.setColumnWidth(0, 80)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(1)
        self.table.setSelectionMode(1)
        self.btn_open.clicked.connect(self.open_mod_folder)
        self.btn_accept.clicked.connect(self.commit_changes)
        self.btn_reset.clicked.connect(self.reset_changes)
        self.check_show_unchanged.clicked.connect(self.show_unchanged)
        # noinspection PyUnresolvedReferences
        self.model.modelReset.connect(self.on_model_reset)

        # noinspection PyUnusedLocal
        def cache_signal_handler(sender, signal_emitter, event: CacheEvent):
            if self.mod is None:
                return
            if str(event.src.abspath()).startswith(str(self.mod.repo.path.abspath())):
                self.model.refresh_data()

        self.cache_signal_handler = cache_signal_handler

    @property
    def mod(self):
        return self.__mod

    @mod.setter
    def mod(self, value):
        self.__mod = value
        self.model.mod = value

    def show_unchanged(self, value: bool):
        self.model.show_unchanged = value
        self.model.refresh_data()

    def on_model_reset(self):
        if self.mod is not None:
            self.set_global_buttons(len(self.mod.repo.status) > 0)

    def set_global_buttons(self, value: bool):
        self.btn_accept.setEnabled(value)
        self.btn_reset.setEnabled(value)

    def commit_changes(self):
        if self.mod is not None:
            commit_msg = LongInputDialog.make(self,
                                              'Describe your changes',
                                              'Write a short summary of the changes you just made:')
            if commit_msg is None:
                return
            self.mod.repo.commit(msg=commit_msg, add_all=True)
            self.model.refresh_data()

    def reset_changes(self):
        if self.mod is None:
            return
        if ConfirmDialog.make('WARNING: resetting this mod will revert all changes made since last commit.\n\n'
                              'This is a destructive operation, and you may loose some of your work.\n\n'
                              'Are you sure you want to continue?'):
            self.mod.repo.hard_reset()
            for x in self.mod.repo.working_dir_new:
                os.remove(os.path.join(self.mod.repo.path.abspath(), x))

    def open_mod_folder(self):
        if self.mod is not None:
            os.startfile(self.mod.repo.path.abspath())

    def showEvent(self, event):
        if self.mod is not None:
            self.setWindowTitle('Showing files for: {}'.format(self.mod.meta.name))
        signals.post_cache_changed_event.connect(self.cache_signal_handler, weak=False)
        self.model.refresh_data()
        super(ModFilesWidget, self).showEvent(event)

    def hideEvent(self, event):
        signals.post_cache_changed_event.disconnect(self.cache_signal_handler)
        super(ModFilesWidget, self).hideEvent(event)