# coding=utf-8

from src.qt import QDialog, dialog_default_flags, QWidget
from src.ui.base.qdialog import BaseDialog
from src.ui.widget_git_files.widget import GitFilesWidget
from src.ui.dialog_own_mod.widget_mod_metadata import ModMetadataWidget
from src.ui.dialog_own_mod.widget_mod_remote import ModRemoteWidget
from src.ui.skeletons.form_mod_details import Ui_Form
from src.mod.mod import Mod
from src.meta_repo.meta_repo import MetaRepo


class _ModDetailsDialog(QDialog, Ui_Form):
    def __init__(self, mod: Mod or None, meta_repo: MetaRepo, parent=None):
        QDialog.__init__(self, parent, flags=dialog_default_flags)
        self.setupUi(self)
        self.__mod = mod
        if mod is not None:
            self.setWindowTitle(mod.meta.name)
        else:
            self.setWindowTitle('Creating new mod')
        self.__meta_repo = meta_repo
        self.metadata_widget = ModMetadataWidget(self.mod, self)
        # self.files_widget = GitFilesWidget(self.mod.repo if self.mod else None, self)
        self.files_widget = GitFilesWidget(self.mod.local_files if self.mod else None, self)  # FIXME
        self.remote_widget = ModRemoteWidget(self.mod, self)
        self.main_layout.addWidget(self.metadata_widget)
        self.main_layout.addWidget(self.files_widget)
        self.main_layout.addWidget(self.remote_widget)
        self.btn_metadata.setChecked(True)
        self.files_widget.setHidden(True)
        self.remote_widget.setHidden(True)
        self.btn_metadata.clicked.connect(lambda: self.show_widget(self.metadata_widget))
        self.btn_local_files.clicked.connect(lambda: self.show_widget(self.files_widget))
        self.btn_remote.clicked.connect(lambda: self.show_widget(self.remote_widget))
        self.mod = mod

    @property
    def meta_repo(self) -> MetaRepo:
        return self.__meta_repo

    @property
    def mod(self):
        return self.__mod

    @mod.setter
    def mod(self, value: Mod):
        self.__mod = value
        if value is None:
            self.btn_local_files.setEnabled(False)
            self.btn_remote.setEnabled(False)
        else:
            self.setWindowTitle(value.meta.name)
            self.btn_local_files.setEnabled(True)
            self.btn_remote.setEnabled(True)
            self.metadata_widget.mod = value
            self.files_widget.repo = value.local_folder  # FIXME
            self.remote_widget.mod = value

    def show_widget(self, widget: QWidget):
        self.metadata_widget.setHidden(True)
        self.files_widget.setHidden(True)
        self.remote_widget.setHidden(True)
        widget.setHidden(False)


class ModDetailsDialog(BaseDialog):
    def __init__(self, mod: Mod or None, meta_repo: MetaRepo, parent=None):
        BaseDialog.__init__(self, _ModDetailsDialog(mod, meta_repo, parent))
        self.qobj.show()

    @staticmethod
    def make(mod: Mod or None, meta_repo: MetaRepo, parent=None):
        dialog = ModDetailsDialog(mod, meta_repo, parent)
        dialog.qobj.show()
        dialog.qobj.exec()
