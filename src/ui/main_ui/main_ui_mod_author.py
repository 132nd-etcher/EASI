# coding=utf-8

from src.cfg import Config
from src.sig import sig_cfg_author_mode, SignalReceiver
from src.ui.skeletons.main import Ui_MainWindow


class MainUiModAuthor:
    def __init__(self, main_ui):
        assert isinstance(main_ui, Ui_MainWindow)
        self.main_ui = main_ui
        self.index = []
        self.config_mapping = {}
        self.receiver = SignalReceiver(self)
        self.receiver[sig_cfg_author_mode] = self.author_mode_changed

    def setup(self):
        self.main_ui.menuMod_authoring.menuAction().setVisible(Config().author_mode)

    def author_mode_changed(self, value: bool):
        self.main_ui.menuMod_authoring.menuAction().setVisible(value)
