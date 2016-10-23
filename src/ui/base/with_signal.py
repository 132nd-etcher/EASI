# coding=utf-8

import abc

from src.sig import CustomSignal, SignalReceiver
from src.low import constants


class WithSignal(metaclass=abc.ABCMeta):
    def __init__(self, sig, main_ui_obj_name):
        if not isinstance(sig, CustomSignal):
            raise TypeError('expected CustomSignal, got: {}'.format(type(sig)))
        if constants.MAIN_UI is None:
            raise RuntimeError('main_ui interface not initialized')
        self.main_ui_obj_name = main_ui_obj_name
        sig.connect(self.on_sig)
        # self.receiver = SignalReceiver(self)
        # self.receiver[sig] = self.on_sig

    def on_sig(self, op: str, *args, **kwargs):
        if not hasattr(constants.MAIN_UI, self.main_ui_obj_name):
            raise AttributeError('main_ui has not attribute "{}"'.format(self.main_ui_obj_name))
        if not hasattr(self, op):
            raise AttributeError('unknown method for {} class: {}'.format(self.__class__.__name__, op))
        constants.MAIN_UI.do(self.main_ui_obj_name, op, *args, **kwargs)
