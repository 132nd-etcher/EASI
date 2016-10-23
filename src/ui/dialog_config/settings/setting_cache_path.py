# coding=utf-8

from blinker import signal

from src.ui.dialog_config.settings.abstract_path_setting import AbstractPathSetting


class CachePathSetting(AbstractPathSetting):

    def __init__(self, dialog):
        AbstractPathSetting.__init__(self, dialog)

        def on_path_changed(_, value):
            self.set_dialog_value(value)

        signal('Config_cache_path_value_changed').connect(on_path_changed, weak=False)

    @property
    def value_name(self) -> str:
        return 'cache_path'

    @property
    def qt_object(self):
        return self.dialog.cache_line_edit

    @property
    def value_display_name(self) -> str:
        return 'cache'

    @property
    def qt_menu_btn(self) -> str:
        return self.dialog.btn_cache
