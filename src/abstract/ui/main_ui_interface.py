# coding=utf-8
import abc


class AbstractMainUiInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def show(self):
        """Show the MainUi"""

    @abc.abstractmethod
    def hide(self):
        """Hides the MainUi"""

    @abc.abstractmethod
    def exit(self):
        """Raises SystemExit"""
