# coding=utf-8

from src.sig import sig_cfg_author_mode, SignalReceiver, sig_config_changed
from src.ui.dialog_disclaimer.dialog import DisclaimerDialog
from src.ui.dialog_config.settings.abstract_config import AbstractConfigSetting
from blinker_herald import emit


class AuthorModeSetting(AbstractConfigSetting):

    @property
    def value_name(self) -> str:
        return 'author_mode'

    @property
    def qt_object(self):
        return self.dialog.author_mode

    def dialog_has_changed_methods(self) -> list:
        return [self.dialog.author_mode.clicked]

    def setup(self):
        self.receiver = SignalReceiver(self)
        self.receiver[sig_cfg_author_mode] = self.author_mode_changed
        self.dialog.tabWidget.setTabEnabled(1, self.value)
        self.dialog.tabWidget.setStyleSheet(
            "QTabBar::tab::disabled {width: 0; height: 0; margin: 0; padding: 0; border: none;} ")

    def save_to_meta(self):
        if self.get_value_from_dialog():
            if DisclaimerDialog.make_for_mod_authors():
                return super(AuthorModeSetting, self).save_to_meta()
            else:
                self.set_dialog_value(False)
        else:
            return super(AuthorModeSetting, self).save_to_meta()

    def get_value_from_dialog(self):
        return self.dialog.author_mode.isChecked()

    def validate_dialog_value(self) -> bool:
        return True

    def set_dialog_value(self, value):
        self.dialog.author_mode.setChecked(self.value)

    @emit()
    def author_mode_changed(self, value: bool, **_):
        self.dialog.tabWidget.setTabEnabled(1, value)
        self.dialog.tabWidget.setStyleSheet(
            "QTabBar::tab::disabled {width: 0; height: 0; margin: 0; padding: 0; border: none;} ")
        self.dialog.author_mode.setChecked(value)
        sig_config_changed.send()
