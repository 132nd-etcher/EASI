# coding=utf-8
from src.ui.dialog_config.settings.abstract_path_setting import AbstractPathSetting
from src.sig import sig_cfg_sg_path


class SGPathSetting(AbstractPathSetting):

    @property
    def value_name(self) -> str:
        return 'saved_games_path'

    def __init__(self, dialog):
        AbstractPathSetting.__init__(self, dialog, sig_cfg_sg_path)

    @property
    def qt_object(self):
        return self.dialog.sg_line_edit

    @property
    def value_display_name(self) -> str:
        return 'Saved Games'

    @property
    def qt_menu_btn(self) -> str:
        return self.dialog.btn_sg
