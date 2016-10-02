# coding=utf-8

import abc

from src.abstract.ui.base_qobject import AbstractBaseQObject
from src.qt import *


class AbstractBaseDialog(AbstractBaseQObject, metaclass=abc.ABCMeta):
    def __init__(self, dialog: QDialog):
        if not isinstance(dialog, QDialog):
            raise TypeError('dialog should be an instance of QDialog, got: {}'.format(type(dialog)))
        AbstractBaseQObject.__init__(self, dialog)

    def show(self, title: str = None, text: str = None):
        self.qobj.setWindowTitle(title)
        self.qobj.label.setText(text)
        self.adjust_size()
        super(AbstractBaseDialog, self).show()

    @staticmethod
    def make(*args, **kwargs):
        raise NotImplementedError('use signals instead')
