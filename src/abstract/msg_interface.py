# coding=utf-8

import abc


class MsgInterface():
    @abc.abstractmethod
    def show(self, title: str, text: str):
        """"""
