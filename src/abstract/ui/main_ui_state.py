# coding=utf-8

import abc


class AbstractMainUiState(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def show_msg(self, title: str, text: str, over_splash: bool = False):
        """"""

    @abc.abstractmethod
    def set_current_state(self, state: str):
        """pass"""

    @staticmethod
    @abc.abstractmethod
    def set_progress(state_manager, value: int):
        """Sets current op progress"""

    @staticmethod
    @abc.abstractmethod
    def set_progress_title(state_manager, value: str):
        """"""

    @staticmethod
    @abc.abstractmethod
    def set_progress_text(state_manager, value: str):
        """"""

    @staticmethod
    @abc.abstractmethod
    def add_progress(state_manager, value: int):
        """Sets current op progress"""
