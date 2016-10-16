# coding=utf-8

from .interface import interfaced_method, InterfacedSignal
from src.abstract.ui import AbstractMsgbox


class MsgboxSig(InterfacedSignal, AbstractMsgbox):

    @interfaced_method
    def show(self, title: str, text: str, over_splash: bool = False):
        """"""
