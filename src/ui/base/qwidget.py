# coding=utf-8


import abc

from src.qt import QWidget
from src.sig import CustomSignal, SignalReceiver

main_ui = None


class BaseQWidget(metaclass=abc.ABCMeta):
    def __init__(self, sig, main_ui_obj_name, qobj: QWidget):
        if not isinstance(qobj, QWidget):
            raise TypeError('qobj should be an instance of QWidget, got: {}'.format(type(qobj)))
        self.__qobj = qobj
        if not isinstance(sig, CustomSignal):
            raise TypeError('expected CustomSignal, got: {}'.format(type(sig)))
        if main_ui is None:
            raise RuntimeError('main_ui interface not initialized')
        self.main_ui_obj_name = main_ui_obj_name
        self.receiver = SignalReceiver(self)
        self.receiver[sig] = self.on_sig

    def on_sig(self, op: str, *args, **kwargs):
        if not hasattr(main_ui, self.main_ui_obj_name):
            raise AttributeError('main_ui has not attribute "{}"'.format(self.main_ui_obj_name))
        if not hasattr(self, op):
            raise AttributeError('unknown method for {} class: {}'.format(self.__class__.__name__, op))
        main_ui.sig_proc.do(self.main_ui_obj_name, op, *args, **kwargs)

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
