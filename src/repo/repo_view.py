# coding=utf-8


from src.repo.repo import Repo
from src.ui.abstract.itable_view_row import ITableViewRow, QColor


class RepoView(ITableViewRow):
    def __init__(self, repo: Repo):
        self.__repo = repo

    @property
    def display_role(self) -> list:
        return [
            self.__repo.user_name,
            self.__repo.push_perm
        ]

    @property
    def foreground_role(self) -> QColor:
        if self.__repo.has_changed:
            return QColor('blue')
        else:
            return QColor('black')

    @property
    def user_role(self) -> object:
        return self.__repo
