# coding=utf-8

from src.qt import QDialog, dialog_default_flags, QWidget
from src.ui.base.qdialog import BaseDialog
from src.ui.widget_git_files.widget import GitFilesWidget
from src.ui.dialog_own_mod.widget_mod_metadata import ModMetadataWidget
from src.ui.dialog_own_mod.widget_mod_remote import ModRemoteWidget
from src.ui.skeletons.form_mod_details import Ui_Form
from src.mod.mod import Mod


class _ModDetailsDialog(QDialog, Ui_Form):
    def __init__(self, mod: Mod or None, parent=None):
        QDialog.__init__(self, parent, flags=dialog_default_flags)
        self.setupUi(self)
        self.__mod = mod
        self.metadata_widget = ModMetadataWidget(self.mod, self)
        self.files_widget = GitFilesWidget(self.mod.repo, self)
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
    def mod(self):
        return self.__mod

    @mod.setter
    def mod(self, value):
        self.__mod = value
        if value is None:
            self.btn_local_files.setEnabled(False)
            self.btn_remote.setEnabled(False)
        else:
            self.btn_local_files.setEnabled(True)
            self.btn_remote.setEnabled(True)
            self.metadata_widget.mod = value
            self.files_widget.mod = value
            self.remote_widget.mod = value

    def show_widget(self, widget: QWidget):
        self.metadata_widget.setHidden(True)
        self.files_widget.setHidden(True)
        self.remote_widget.setHidden(True)
        widget.setHidden(False)


class ModDetailsDialog(BaseDialog):
    def __init__(self, mod: Mod or None, parent=None):
        BaseDialog.__init__(self, _ModDetailsDialog(mod, parent))
        self.qobj.show()
