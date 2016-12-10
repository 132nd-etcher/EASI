# coding=utf-8

from src.cfg.cfg import Config
from blinker import signal
from src.ui.skeletons.main import Ui_MainWindow


class MainUiModAuthor:
    def __init__(self, main_ui):
        assert isinstance(main_ui, Ui_MainWindow)
        self.main_ui = main_ui
        self.index = []
        self.config_mapping = {}

        # noinspection PyUnusedLocal
        def author_mode_changed(sender, value: bool):
            self.main_ui.menuMod_authoring.menuAction().setVisible(value)

        signal('Config_author_mode_value_changed').connect(author_mode_changed, weak=False)

    def setup(self):
        self.main_ui.menuMod_authoring.menuAction().setVisible(Config().author_mode)
