# coding=utf-8

import abc

from PyQt5.QtCore import QObject


class AbstractBaseQObject(metaclass=abc.ABCMeta):
    def __init__(self, qobj: QObject):
        if not isinstance(qobj, QObject):
            raise TypeError('qobj should be an instance of QObject, got: {}'.format(type(qobj)))
        self.qobj = qobj

    def show(self):
        self.qobj.show()

    def hide(self):
        self.qobj.hide()

    def adjust_size(self):
        self.qobj.adjustSize()
        # self.qobj.setFixedSize(
        #     self.qobj.width(),
        #     self.qobj.height(),
        # )
