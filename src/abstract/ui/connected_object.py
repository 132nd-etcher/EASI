# coding=utf-8

import abc

main_ui = None


class AbstractConnectedObject(metaclass=abc.ABCMeta):
    def __init__(self, sig, main_ui_obj_name):
        from src.sig import SignalReceiver, CustomSignal
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
