# coding=utf-8

from src.cfg import config
from src.low.custom_logging import make_logger
from src.qt import QDialog, Qt, QStyleFactory
from src.ui.dialog_config.abstract_config_dialog_child import AbstractConfigDialogChild
from src.ui.dialog_config.settings_gh import GHSettings
from src.ui.dialog_config.settings_mod_authoring import ModAuthoringSettings
from src.ui.dialog_config.settings_paths import PathsSettings
from src.ui.skeletons.config_dialog import Ui_Settings
from src.upd import check_for_update

logger = make_logger(__name__)


class ConfigDialog(Ui_Settings, QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent, flags=Qt.WindowSystemMenuHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        Ui_Settings.__init__(self)
        self.main_ui = parent
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(self.buttonBox.Apply).clicked.connect(self.save_settings)
        self.buttonBox.button(self.buttonBox.Reset).clicked.connect(self.load_settings)
        self.btn_update_check.clicked.connect(check_for_update)
        self.gh_settings = GHSettings(self)
        self.path_settings = PathsSettings(self)
        self.mod_authoring_settings = ModAuthoringSettings(self)
        self.settings_children = [
            self.path_settings,
            self.mod_authoring_settings,
            self.gh_settings
        ]
        f_style = QStyleFactory()
        self.comboBox.addItems(f_style.keys())
        self.comboBox.activated[str].connect(self.set_style)

    def show(self):
        self.gh_settings.dialog.githubPasswordLineEdit.setText('')
        self.gh_settings.dialog.githubUsernameLineEdit.setText('')
        self.load_settings()
        super(ConfigDialog, self).show()

    def setup(self):
        self.load_settings()
        for child in self.settings_children:
            assert isinstance(child, AbstractConfigDialogChild)
            child.setup()

    @staticmethod
    def set_style(style):
        import blinker
        sig = blinker.signal('sig_main_ui_style')
        print(style)
        sig.send('dialog_config', style=style)

    def load_settings(self):
        self.subscribe_to_test_versions.setChecked(config.subscribe_to_test_versions)
        self.author_mode.setChecked(config.author_mode)
        for child in self.settings_children:
            assert isinstance(child, AbstractConfigDialogChild)
            child.load_settings()

    def save_settings(self):
        success = True
        config.subscribe_to_test_versions = self.subscribe_to_test_versions.isChecked()
        config.author_mode = self.author_mode.isChecked()
        for child in self.settings_children:
            assert isinstance(child, AbstractConfigDialogChild)
            success = success and child.save_settings()
        return success

    def reject(self):
        super(ConfigDialog, self).reject()
        self.hide()

    def accept(self):
        if self.save_settings():
            super(ConfigDialog, self).accept()
            self.hide()

    @staticmethod
    def make():
        raise NotImplementedError('use main_ui or signals')
