# coding=utf-8

import abc


class AbstractMainUiState(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def set_current_state(self, state: str):
        """pass"""

    @staticmethod
    @abc.abstractmethod
    def updater_started(state_manager):
        """Fires when EASI updater starts"""

    @staticmethod
    @abc.abstractstaticmethod
    def updater_finished(state_manager):
        """Fires when EASI updater finishes"""

    @staticmethod
    @abc.abstractstaticmethod
    def dcs_installs_lookup_start(state_manager):
        """Fires when EASI is looking for local DCS installations"""

    @staticmethod
    @abc.abstractstaticmethod
    def dcs_installs_lookup_finished(state_manager):
        """Fires when EASI is looking for local DCS installations"""

    @staticmethod
    @abc.abstractstaticmethod
    def keyring_validation_start(state_manager):
        """Fires when EASI is looking for local DCS installations"""

    @staticmethod
    @abc.abstractstaticmethod
    def keyring_validation_finished(state_manager):
        """Fires when EASI is looking for local DCS installations"""

    @staticmethod
    @abc.abstractmethod
    def set_progress(state_manager, value: int):
        """Sets current op progress"""

    @staticmethod
    @abc.abstractmethod
    def add_progress(state_manager, value: int):
        """Sets current op progress"""
