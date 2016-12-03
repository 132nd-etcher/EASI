# coding=utf-8

import abc

from src.abstract.msg_interface import MsgInterface


class MsgboxInterface(MsgInterface):
    @abc.abstractmethod
    def show(self, title: str, text: str):
        """"""

    @abc.abstractmethod
    def error(self, text: str):
        """"""
