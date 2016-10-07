# coding=utf-8
from src.ui.dialog_config.settings.abstract_path_setting import AbstractPathSetting


class SGPathSetting(AbstractPathSetting):

    def __init__(self, dialog, value_name: str):
        AbstractPathSetting.__init__(self, dialog, value_name)

    def show(self):
        pass

    @property
    def qt_object(self):
        return self.dialog.sg_line_edit

    def dir_name(self) -> str:
        return 'Saved Games'

    @property
    def qt_menu_btn(self) -> str:
        return self.dialog.btn_sg
