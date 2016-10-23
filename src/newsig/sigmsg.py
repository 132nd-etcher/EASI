# coding=utf-8

from src.abstract.msg_interface import MsgInterface
from src.newsig.metacustomsig import MetaCustomSig


class SigMsg(MsgInterface, metaclass=MetaCustomSig):
    def show(self, title: str, text: str):
        pass
