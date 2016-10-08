# coding=utf-8

from src.ui.dialog_config.settings.abstract_config import AbstractConfigSetting


class KeyringEncryptSetting(AbstractConfigSetting):
    @property
    def value_name(self) -> str:
        return 'encrypt_keyring'

    @property
    def qt_object(self):
        return self.dialog.check_box_encrypt

    def dialog_has_changed_methods(self) -> list:
        return [self.dialog.check_box_encrypt.clicked]

    def setup(self):
        pass

    def get_value_from_dialog(self):
        return self.dialog.check_box_encrypt.isChecked()

    def validate_dialog_value(self) -> bool:
        return True

    def set_dialog_value(self, value):
        self.dialog.check_box_encrypt.setChecked(self.value)
