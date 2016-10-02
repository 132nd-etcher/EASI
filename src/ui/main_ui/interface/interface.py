# coding=utf-8
from src.abstract.ui.main_ui_interface import AbstractMainUiInterface
from src.sig import sig_main_ui, SignalReceiver
from src.ui.main_ui.interface.wrapper import interfaced_method


class MainUiSigProcessor(AbstractMainUiInterface):

    main_ui = None

    def __init__(self, main_ui):
        MainUiSigProcessor.main_ui = main_ui
        self.receiver = SignalReceiver(self)
        self.receiver[sig_main_ui] = self.on_sig

    def on_sig(self, op: str, *args, **kwargs):
        if not hasattr(self, op):
            raise ValueError('unknown method for {}: {}'.format(self.__class__.__name__, op))
        self.do(None, op, *args, **kwargs)

    @classmethod
    def do(cls, *args, **kwargs):
        if MainUiSigProcessor.main_ui is None:
            raise Exception('main_ui interface not initialized')
        MainUiSigProcessor.main_ui.do(*args, **kwargs)

    @classmethod
    @interfaced_method(None)
    def show(cls):
        """pass"""

    @classmethod
    @interfaced_method(None)
    def hide(cls):
        """pass"""


    @classmethod
    @interfaced_method(None)
    def exit(self):
        """pass"""
