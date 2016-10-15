# coding=utf-8

import abc

from src.qt import QWidget


class AbstractBaseQWidget(metaclass=abc.ABCMeta):
    def __init__(self, qobj: QWidget):
        if not isinstance(qobj, QWidget):
            raise TypeError('qobj should be an instance of QObject, got: {}'.format(type(qobj)))
        self.qobj = qobj

    def show(self):
        self.qobj.show()
        self.adjust_size()

    def hide(self):
        self.qobj.hide()

    def adjust_size(self):
        self.qobj.setMaximumSize(400, 16777215)
        self.qobj.adjustSize()
        self.qobj.setFixedSize(
            self.qobj.width() + 20,
            self.qobj.height(),
        )
