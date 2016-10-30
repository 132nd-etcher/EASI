# coding=utf-8

import os

from blinker_herald import signals

from src.cache.cache import CacheEvent
from src.mod.mod_objects.mod_base import BaseMod
from src.qt import QAbstractTableModel, QDialog, dialog_default_flags, Qt, QModelIndex, QVariant, QIcon, \
    qt_resources, QSortFilterProxyModel, QColor
from src.ui.base.qdialog import BaseDialog
from src.ui.dialog_confirm.dialog import ConfirmDialog
from src.ui.dialog_long_input.dialog import LongInputDialog
from src.ui.skeletons.dialog_single_mod_view import Ui_Dialog


class SingleModModel(QAbstractTableModel):
    def __init__(self, mod: BaseMod, parent):
        QAbstractTableModel.__init__(self, parent)
        self.__data = []
        self.mod = mod
        self.show_unchanged = True

    def refresh_data(self):
        if self.mod is not None:
            self.beginResetModel()
            self.__data = []
            assert isinstance(self.mod, BaseMod)
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
            print(self.show_unchanged)
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
        return super(SingleModModel, self).headerData(column, orientation, role)


class _SingleModViewDialog(QDialog, Ui_Dialog):
    def __init__(self, mod: BaseMod, parent=None):
        QDialog.__init__(self, parent, flags=dialog_default_flags)
        self.setupUi(self)
        self.setWindowIcon(QIcon(qt_resources.app_ico))
        self.mod = mod
        self.setWindowTitle('Showing single mod: {}'.format(mod.name))
        self.model = SingleModModel(mod, self)
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
        # noinspection PyUnresolvedReferences
        self.model.modelReset.connect(self.on_model_reset)
        self.check_hide_unchanged.clicked.connect(self.hide_unchanged)
        self.btn_done.clicked.connect(self.accept)

        # noinspection PyUnusedLocal
        def filter_cache_sig(sender, signal_emitter, event: CacheEvent):
            if str(event.src.abspath()).startswith(str(self.mod.repo.path.abspath())):
                self.model.refresh_data()

        self.signal_handler = filter_cache_sig

    def hide_unchanged(self, value: bool):
        self.model.show_unchanged = not value
        self.model.refresh_data()

    def on_model_reset(self):
        self.set_global_buttons(len(self.mod.repo.status) > 0)

    def set_global_buttons(self, value: bool):
        self.btn_accept.setEnabled(value)
        self.btn_reset.setEnabled(value)

    def commit_changes(self):
        commit_msg = LongInputDialog.make(self,
                                          'Describe your changes',
                                          'Write a short summary of the changes you just did:')
        if commit_msg is None:
            return
        self.mod.repo.commit(msg=commit_msg, add_all=True)
        self.model.refresh_data()

    def reset_changes(self):
        if ConfirmDialog.make('WARNING: resetting this mod will revert all changes made since last commit.\n\n'
                              'This is a destructive operation, and you may loose some of your work.\n\n'
                              'Are you sure you want to continue?'):
            self.mod.repo.hard_reset()
            for x in self.mod.repo.working_dir_new:
                os.remove(os.path.join(self.mod.repo.path.abspath(), x))

    def open_mod_folder(self):
        os.startfile(self.mod.repo.path.abspath())

    def show(self):
        signals.post_cache_changed_event.connect(self.signal_handler, weak=False)
        self.model.refresh_data()
        super(_SingleModViewDialog, self).show()

    def accept(self):
        signals.post_cache_changed_event.disconnect(self.signal_handler)
        super(_SingleModViewDialog, self).accept()


class SingleModViewDialog(BaseDialog):
    def __init__(self, mod, parent=None):
        BaseDialog.__init__(self, _SingleModViewDialog(mod, parent))
        self.qobj.show()

    @property
    def qobj(self) -> _SingleModViewDialog:
        return super(SingleModViewDialog, self).qobj
