# coding=utf-8
import abc


class ProgressInterface():

    @abc.abstractmethod
    def set_progress(self, value: int):
        """Sets the progress bar to 'value' """

    @abc.abstractmethod
    def add_progress(self, value: int):
        """Sets the progress bar to 'value' """

    @abc.abstractmethod
    def set_progress_title(self, value: str):
        """Sets the progress main title"""

    @abc.abstractmethod
    def set_progress_text(self, value: str):
        """Sets the progress bar text"""

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

    @abc.abstractmethod
    def show(self, title: str, text: str, auto_close: bool = True):
        """Sets the progress bar to 'value' """

    @abc.abstractmethod
    def hide(self):
        """Sets the progress bar to 'value' """
