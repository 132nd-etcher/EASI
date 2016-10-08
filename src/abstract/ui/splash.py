# coding=utf-8
import abc


class AbstractSplash(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get(self):
        """"""

    @abc.abstractmethod
    def get_progress(self):
        """"""

    @abc.abstractmethod
    def current_progress(self):
        """"""

    @abc.abstractmethod
    def add_to_progress(self, value: int):
        """"""

    @abc.abstractmethod
    def show(self):
        """"""

    @abc.abstractmethod
    def kill(self):
        """"""

    @abc.abstractmethod
    def set_progress(self, value: int):
        """"""

    @abc.abstractmethod
    def set_progress_text(self, value: str):
        """"""
