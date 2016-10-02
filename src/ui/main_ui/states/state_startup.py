# coding=utf-8

from src.abstract.ui.main_ui_state import AbstractMainUiState

from src.low.constants import APP_SHORT_NAME
from src.sig import sig_splash


class UiStateStartup(AbstractMainUiState):
    @staticmethod
    def set_progress(state_manager, value: int):
        sig_splash.set_progress(value)

    @staticmethod
    def add_progress(state_manager, value: int):
        sig_splash.add_to_progress(value)

    @staticmethod
    def keyring_validation_finished(state_manager):
        sig_splash.set_progress(100)

    @staticmethod
    def keyring_validation_start(state_manager):
        sig_splash.set_progress(0)
        sig_splash.set_text('Validating credentials')

    @staticmethod
    def dcs_installs_lookup_finished(state_manager):
        sig_splash.set_progress(100)

    @staticmethod
    def dcs_installs_lookup_start(state_manager):
        sig_splash.set_progress(0)
        sig_splash.set_text('Looking for DCS installations')

    @staticmethod
    def updater_finished(state_manager):
        sig_splash.set_progress(100)

    @staticmethod
    def updater_started(state_manager):
        sig_splash.set_progress(0)
        sig_splash.set_text('Looking for a newer version of {}'.format(APP_SHORT_NAME))
