# coding=utf-8
import abc

from src.abstract.abstract_progress import ProgressInterface


class AbstractLongOp(ProgressInterface, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def show(self, title: str, text: str):
        """Sets the progress bar to 'value' """

    @abc.abstractmethod
    def hide(self):
        """Sets the progress bar to 'value' """


class AbstractLongOpDual(AbstractLongOp, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def set_current_progress(self, value: int):
        """Sets the current progress bar to 'value' """

    @abc.abstractmethod
    def add_current_progress(self, value: int):
        """Sets the current progress bar to 'value' """

    @abc.abstractmethod
    def set_current_text(self, value: str):
        """Sets the current op label"""
