# coding=utf-8
from blinker import signal

from src.ui.dialog_config.settings.abstract_path_setting import AbstractPathSetting


class SGPathSetting(AbstractPathSetting):
    @property
    def value_name(self) -> str:
        return 'saved_games_path'

    def __init__(self, dialog):
        AbstractPathSetting.__init__(self, dialog)

        def on_path_changed(_, value):
            self.set_dialog_value(value)

        signal('Config_saved_games_path_value_changed').connect(on_path_changed, weak=False)

    @property
    def qt_object(self):
        return self.dialog.sg_line_edit

    @property
    def value_display_name(self) -> str:
        return 'Saved Games'

    @property
    def qt_menu_btn(self) -> str:
        return self.dialog.btn_sg
