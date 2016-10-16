# coding=utf-8

import abc


class AbstractMsgbox(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def show(self, title: str, text: str, over_splash: bool = False):
        """"""
