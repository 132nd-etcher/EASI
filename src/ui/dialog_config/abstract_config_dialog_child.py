# coding=utf-8

import abc


class AbstractConfigDialogChild(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def save_settings(self):
        """Save settings to the config file"""

    @abc.abstractmethod
    def load_settings(self):
        """Loads settings from the config file"""

    @abc.abstractmethod
    def setup(self):
        """Set up the child dialog"""
