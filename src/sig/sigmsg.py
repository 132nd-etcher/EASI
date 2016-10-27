# coding=utf-8

from src.abstract.msg_interface import MsgInterface
from src.sig.customsig import CustomSig


class SigMsg(MsgInterface, metaclass=CustomSig):
    def show(self, title: str, text: str):
        pass
