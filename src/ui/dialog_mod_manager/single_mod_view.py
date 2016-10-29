# coding=utf-8

import os

from blinker_herald import signals

from src.cache.cache import CacheEvent
from src.mod.mod_objects.mod_draft import ModDraft
from src.qt import QAbstractTableModel, QDialog, dialog_default_flags, Qt, QModelIndex, QVariant, QIcon, \
    qt_resources
from src.ui.base.qdialog import BaseDialog
from src.ui.dialog_long_input.dialog import LongInputDialog
from src.ui.skeletons.dialog_single_mod_view import Ui_Dialog
from src.ui.dialog_confirm.dialog import ConfirmDialog


class SingleModModel(QAbstractTableModel):
    def __init__(self, parent):
        QAbstractTableModel.__init__(self, parent)
        self.__data = []
        self.__mod = None

    @property
    def mod(self) -> ModDraft:
        return self.__mod

    @mod.setter
    def mod(self, value: ModDraft):
        self.__mod = value

    def refresh_data(self):
        if self.mod is not None:
            self.beginResetModel()
            self.__data = []
            assert isinstance(self.mod, ModDraft)
            for x in self.mod.repo.working_dir_new:
                self.__data.append(('new', x))
            for x in self.mod.repo.working_dir_modified:
                self.__data.append(('modified', x))
            for x in self.mod.repo.working_dir_deleted:
                self.__data.append(('deleted', x))
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


class _SingleModViewDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent, flags=dialog_default_flags)
        self.setupUi(self)
        self.setWindowIcon(QIcon(qt_resources.app_ico))
        self.model = SingleModModel(self)
        self.table.setModel(self.model)
        self.table.horizontalHeader().hide()
        self.table.verticalHeader().hide()
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(1)
        self.table.setSelectionMode(1)
        self.btn_open.clicked.connect(self.open_mod_folder)
        self.btn_accept.clicked.connect(self.commit_changes)
        self.btn_reset.clicked.connect(self.reset_changes)
        self.model.modelReset.connect(self.on_model_reset)

    def on_model_reset(self):
        self.set_global_buttons(self.model.rowCount() > 0)

    def set_global_buttons(self, value: bool):
        self.btn_accept.setEnabled(value)
        self.btn_reset.setEnabled(value)

    @property
    def mod(self) -> ModDraft:
        return self.model.mod

    @mod.setter
    def mod(self, value: ModDraft):
        self.setWindowTitle('Showing single mod: {}'.format(value.name))
        self.model.mod = value

    def commit_changes(self):
        commit_msg = LongInputDialog.make(self,
                                          'Describe your changes',
                                          'Write a short summary of the changes you just did:')
        if commit_msg is None:
            return
        self.mod.repo.commit(msg=commit_msg, add_all=True)

    def reset_changes(self):
        if ConfirmDialog.make('WARNING: resetting this mod will revert all changes made since last commit.\n\n'
                              'This is a destructive operation, and you may loose some of your work.\n\n'
                              'Are you sure you want to continue?'):
            self.mod.repo.hard_reset()

    def open_mod_folder(self):
        os.startfile(self.mod.repo.path.abspath())

    def show(self):
        def filter_cache_sig(sender, signal_emitter, event: CacheEvent):
            if str(event.src.abspath()).startswith(str(self.mod.repo.path.abspath())):
                self.model.refresh_data()

        signals.post_cache_changed_event.connect(filter_cache_sig, weak=False)
        super(_SingleModViewDialog, self).show()

    def close(self):
        super(_SingleModViewDialog, self).close()


class SingleModViewDialog(BaseDialog):
    def __init__(self, parent=None):
        BaseDialog.__init__(self, _SingleModViewDialog(parent))
        self.qobj.show()

    @property
    def qobj(self) -> _SingleModViewDialog:
        return super(SingleModViewDialog, self).qobj


if __name__ == '__main__':
    from src.qt import QApplication
    from src.cache.cache import Cache
    from src.rem.gh.gh_session import GHSession
    from src.keyring.keyring import Keyring

    GHSession(Keyring().gh_token)
    Cache('./cache')
    qt_app = QApplication([])
    mod = ModDraft('CbUJymJsYznX6b7SCoajza')
    dialog = SingleModViewDialog()
    dialog.qobj.mod = mod
    dialog.qobj.model.refresh_data()
    exit(dialog.qobj.exec())
