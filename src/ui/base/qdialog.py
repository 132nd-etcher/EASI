# coding=utf-8

import abc
from src.qt import QDialog
from .qwidget import BaseQWidget


class BaseDialog(BaseQWidget, metaclass=abc.ABCMeta):
    def __init__(self, sig, main_ui_obj_name, qobj: QDialog):
        if not isinstance(qobj, QDialog):
            raise TypeError('dialog should be an instance of QDialog, got: {}'.format(type(qobj)))
        super(BaseDialog, self).__init__(sig, main_ui_obj_name, qobj)

    @property
    def qobj(self) -> QDialog:
        return super(BaseDialog, self).qobj