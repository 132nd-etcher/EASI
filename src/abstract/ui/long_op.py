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
