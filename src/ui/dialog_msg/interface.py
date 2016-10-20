# coding=utf-8

import abc


class MsgboxInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def show(self, title: str, text: str, over_splash: bool = False):
        """"""
