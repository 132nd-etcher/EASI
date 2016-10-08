# coding=utf-8
from src.sig import sig_cache_path_changed
from src.ui.dialog_config.settings.abstract_path_setting import AbstractPathSetting


class CachePathSetting(AbstractPathSetting):
    @property
    def value_name(self) -> str:
        return 'cache_path'

    def __init__(self, dialog):
        AbstractPathSetting.__init__(self, dialog, sig_cache_path_changed)

    @property
    def qt_object(self):
        return self.dialog.cache_line_edit

    def dir_name(self) -> str:
        return 'cache'

    @property
    def qt_menu_btn(self) -> str:
        return self.dialog.btn_cache
