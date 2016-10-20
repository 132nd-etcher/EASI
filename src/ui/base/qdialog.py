# coding=utf-8

import abc
from src.qt import QDialog
from .qwidget import BaseQWidget


class BaseDialog(BaseQWidget, metaclass=abc.ABCMeta):
    def __init__(self, dialog: QDialog):
        if not isinstance(dialog, QDialog):
            raise TypeError('dialog should be an instance of QDialog, got: {}'.format(type(dialog)))
        super(BaseDialog, self).__init__(dialog)

    @property
    def qobj(self) -> QDialog:
        return self.__qobj