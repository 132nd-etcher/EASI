# coding=utf-8
from src.sig import sig_cfg_cache_path
from src.ui.dialog_config.settings.abstract_path_setting import AbstractPathSetting


class CachePathSetting(AbstractPathSetting):
    @property
    def value_name(self) -> str:
        return 'cache_path'

    def __init__(self, dialog):
        AbstractPathSetting.__init__(self, dialog, sig_cfg_cache_path)

    @property
    def qt_object(self):
        return self.dialog.cache_line_edit

    @property
    def value_display_name(self) -> str:
        return 'cache'

    @property
    def qt_menu_btn(self) -> str:
        return self.dialog.btn_cache
