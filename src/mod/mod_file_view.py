# coding=utf-8


from src.mod.mod_file import ModFile
from src.ui.abstract.itable_view_row import ITableViewRow, QColor


class DeletedModFileView(ITableViewRow):
    @property
    def foreground_role(self) -> QColor:
        return QColor('red')

    @property
    def display_role(self) -> list:
        return [
            self.__path,
            '', '', 'deleted', ''
        ]

    @property
    def user_role(self) -> None:
        return None

    def __init__(self, local_file_path):
        self.__path = local_file_path


class ModFileView(ITableViewRow):
    def __init__(self, mod_file: ModFile):
        self.__mod_file = mod_file

    @property
    def display_role(self) -> list:
        return [
            str(self.__mod_file.rel_path),
            self.__mod_file.human_size,
            self.__mod_file.last_changed,
            self.__mod_file.status,
            self.__mod_file.action
        ]

    @property
    def foreground_role(self) -> QColor:
        if self.__mod_file.is_new:
            return QColor('green')
        elif self.__mod_file.is_modified:
            return QColor('blue')
        else:
            return QColor('black')

    @property
    def user_role(self) -> ModFile:
        return self.__mod_file
