# coding=utf-8
from src.ui.dialog_config.settings.abstract_path_setting import AbstractPathSetting
from src.low.custom_path import Path


class SGPathSetting(AbstractPathSetting):

    def validate_dialog_value(self) -> bool:
        p = Path(self.get_value_from_dialog())
        if not p.exists():
            self.show_tooltip('Directory does not exist')
        elif not p.isdir():
            self.show_tooltip('Not a directory')
        else:
            return True

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
