# coding=utf-8

import abc

from src.qt import QColor


class ITableViewRow:

    @property
    @abc.abstractproperty
    def user_role(self) -> object:
        pass

    @property
    @abc.abstractproperty
    def display_role(self) -> list:
        pass

    @property
    @abc.abstractproperty
    def foreground_role(self) -> QColor:
        pass