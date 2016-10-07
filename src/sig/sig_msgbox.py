# coding=utf-8

from .interface import interfaced_method, InterfacedSignal


class MsgboxSig(InterfacedSignal):

    @interfaced_method
    def show(self, title: str, text: str):
        """"""

    @interfaced_method
    def hide(self):
        """"""
