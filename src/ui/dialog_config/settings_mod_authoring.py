# coding=utf-8

from src.cfg import config
from src.sig import sig_author_mode, SignalReceiver
from src.ui.dialog_config.abstract_config_dialog_child import AbstractConfigDialogChild
from src.ui.dialog_disclaimer.dialog import DisclaimerDialog
from src.ui.skeletons.config_dialog import Ui_Settings


class ModAuthoringSettings(AbstractConfigDialogChild):
    def __init__(self, dialog: Ui_Settings):
        self.dialog = dialog
        self.receiver = SignalReceiver(self)
        self.receiver[sig_author_mode] = self.author_mode_changed
        self.dialog.tabWidget.setStyleSheet(
            "QTabBar::tab::disabled {width: 0; height: 0; margin: 0; padding: 0; border: none;} ")

    def setup(self):
        if config.author_mode:
            config.author_mode = DisclaimerDialog.make_for_mod_authors()

    def load_settings(self):
        self.author_mode_changed(config.author_mode)

    def save_settings(self):
        config.author_mode = self.dialog.author_mode.isChecked()
        if config.author_mode:
            config.author_mode = DisclaimerDialog.make_for_mod_authors()
        return True

    def author_mode_changed(self, value: bool, **_):
        self.dialog.tabWidget.setTabEnabled(1, value)
        self.dialog.tabWidget.setStyleSheet(
            "QTabBar::tab::disabled {width: 0; height: 0; margin: 0; padding: 0; border: none;} ")
        self.dialog.author_mode.setChecked(value)
