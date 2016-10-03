# coding=utf-8

import abc

from src.qt import QObject
from .connected_object import AbstractConnectedObject


class AbstractConnectedQObject(AbstractConnectedObject, metaclass=abc.ABCMeta):
    def __init__(self, sig, main_ui_obj_name, qobj: QObject):
        from src.sig import CustomSignal
        if not isinstance(sig, CustomSignal):
            raise TypeError('expected CustomSignal, got: {}'.format(type(sig)))
        AbstractConnectedObject.__init__(self, sig, main_ui_obj_name)
        self.qobj = qobj
