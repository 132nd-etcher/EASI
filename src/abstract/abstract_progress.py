# coding=utf-8
import abc


class ProgressInterface(metaclass=abc.ABCMeta):
    """
    Interface to an object that has:

        - a progress bar
        - a progress label

    """
    @abc.abstractmethod
    def set_progress(self, value: int):
        """Sets the progress bar to 'value' """

    @abc.abstractmethod
    def add_progress(self, value: int):
        """Sets the progress bar to 'value' """

    @abc.abstractmethod
    def set_text(self, value: str):
        """Sets the progress bar to 'value' """

    @abc.abstractmethod
    def set_current_enabled(self, value: bool):
        """Shows or hides the "current" bar and label"""

    @abc.abstractmethod
    def set_current_progress(self, value: int):
        """Sets the progress bar to 'value' """

    @abc.abstractmethod
    def add_current_progress(self, value: int):
        """Sets the progress bar to 'value' """

    @abc.abstractmethod
    def set_current_text(self, value: str):
        """Sets the progress bar to 'value' """
