# coding=utf-8

from src.low import constants
from src.low.custom_logging import make_logger
from src.qt import QDialog, Qt
from src.sig import sig_config_changed, SignalReceiver, sig_msgbox
from src.ui.skeletons.config_dialog import Ui_Settings
from src.upd import check_for_update
from .settings.abstract_config import AbstractConfigSetting
from .settings.abstract_credential import AbstractCredentialSetting
from .settings.setting_author_mode import AuthorModeSetting
from .settings.setting_cache_path import CachePathSetting
from .settings.setting_dropbox import DropboxSetting
from .settings.setting_github import GithubSetting
from .settings.setting_kdiff_path import KDiffPathSetting
from .settings.setting_keyring_encrypt import KeyringEncryptSetting
from .settings.setting_sg_path import SGPathSetting
from .settings.setting_update_to_experimental import ExperimentalUpdateSetting

logger = make_logger(__name__)


class ConfigDialog(Ui_Settings, QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent, flags=Qt.WindowSystemMenuHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        Ui_Settings.__init__(self)
        self.main_ui = parent
        self.setupUi(self)
        self.btn_apply = self.buttonBox.button(self.buttonBox.Apply)
        self.btn_reset = self.buttonBox.button(self.buttonBox.Reset)
        self.btn_ok = self.buttonBox.button(self.buttonBox.Ok)
        self.btn_cancel = self.buttonBox.button(self.buttonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.btn_apply.clicked.connect(self.apply_clicked)
        self.btn_reset.clicked.connect(self.reset_clicked)
        self.btn_ok.clicked.connect(self.ok_clicked)
        self.btn_cancel.clicked.connect(self.cancel_clicked)
        self.btn_update_check.clicked.connect(self.__check_for_update)
        self.config_settings = {
            'encrypt_keyring': KeyringEncryptSetting(self),
            'author_mode': AuthorModeSetting(self),
            'test_update': ExperimentalUpdateSetting(self),
            'sg_path': SGPathSetting(self),
            'cache_path': CachePathSetting(self),
            'kdiff_path': KDiffPathSetting(self),
        }
        self.keyring_settings = {
            'dropbox': DropboxSetting(self),
            'github': GithubSetting(self),
        }
        self.receiver = SignalReceiver(self)
        self.receiver[sig_config_changed] = self.settings_changed

    def __set_apply_btn_enabled(self, value: bool):
        self.btn_apply.setEnabled(value)

    @staticmethod
    def __check_for_update():
        check_for_update()
        sig_msgbox.show('Check done', 'Already running latest version of {}'.format(constants.APP_SHORT_NAME))

    def show(self):
        for config_setting in self.config_settings.values():
            config_setting.show()
        for keyring_setting in self.keyring_settings.values():
            keyring_setting.show()

        self.load_settings()
        self.__set_apply_btn_enabled(False)
        super(ConfigDialog, self).show()

    def setup(self):
        for setting in self.config_settings.values():
            assert isinstance(setting, AbstractConfigSetting)
            setting.setup()
            for method in setting.dialog_has_changed_methods():
                self.receiver[method] = self.settings_changed
        for setting in self.keyring_settings.values():
            assert isinstance(setting, AbstractCredentialSetting)
            setting.setup()
        self.load_settings()

    def load_settings(self):
        for setting in self.config_settings.values():
            assert isinstance(setting, AbstractConfigSetting)
            setting.load_from_meta()
        self.__set_apply_btn_enabled(False)

    def ok_clicked(self):
        self.accept()

    def reset_clicked(self):
        self.load_settings()

    def cancel_clicked(self):
        self.reject()

    def apply_clicked(self):
        self.save_settings()

    def save_settings(self):
        for setting in self.config_settings.values():
            assert isinstance(setting, AbstractConfigSetting)
            if not setting.save_to_meta():
                return False
        self.__set_apply_btn_enabled(False)
        return True

    def reject(self):
        super(ConfigDialog, self).reject()
        self.hide()

    def accept(self):
        if self.save_settings():
            super(ConfigDialog, self).accept()
            self.hide()

    def settings_changed(self):
        self.__set_apply_btn_enabled(False)
        for setting in self.config_settings.values():
            if setting.has_changed:
                self.__set_apply_btn_enabled(True)
            else:
                setting.validation_success()

    @staticmethod
    def make():
        raise NotImplementedError('use main_ui or signals')
