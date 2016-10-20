# coding=utf-8


import abc

from src.qt import QWidget


class BaseQWidget(metaclass=abc.ABCMeta):
    def __init__(self, qobj: QWidget):
        if not isinstance(qobj, QWidget):
            raise TypeError('qobj should be an instance of QWidget, got: {}'.format(type(qobj)))
        self.__qobj = qobj

    @property
    def qobj(self) -> QWidget:
        return self.__qobj

    def adjust_size(self):
        self.qobj.setMaximumSize(400, 16777215)
        self.qobj.adjustSize()

    def fix_size(self):
        self.adjust_size()
        self.qobj.setFixedSize(
            self.qobj.width() + 20,
            self.qobj.height(),
        )
