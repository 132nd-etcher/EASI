# coding=utf-8

import abc

from src.abstract.ui.base_qobject import AbstractBaseQWidget
from src.qt import QDialog


class AbstractBaseDialog(AbstractBaseQWidget, metaclass=abc.ABCMeta):
    def __init__(self, dialog: QDialog):
        if not isinstance(dialog, QDialog):
            raise TypeError('dialog should be an instance of QDialog, got: {}'.format(type(dialog)))
        AbstractBaseQWidget.__init__(self, dialog)

    @staticmethod
    def make(*args, **kwargs):
        raise NotImplementedError('use signals instead')
