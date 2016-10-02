# coding=utf-8

from src.abstract.ui import AbstractMainUiState

from src.low import constants
from src.sig import sig_long_op_dialog
from src.ui.dialog_msg.dialog import MsgDialog


class UiStateRunning(AbstractMainUiState):
    @staticmethod
    def set_progress(state_manager, value: int):
        sig_long_op_dialog.set_progress(value)

    @staticmethod
    def add_progress(state_manager, value: int):
        sig_long_op_dialog.add_progress(value)

    @staticmethod
    def keyring_validation_finished(state_manager):
        # TODO
        print('keyring_validation_finished')

    @staticmethod
    def keyring_validation_start(state_manager):
        # TODO
        print('keyring_validation_start')

    @staticmethod
    def dcs_installs_lookup_finished(state_manager):
        # TODO
        print('dcs_installs_lookup_finished')

    @staticmethod
    def dcs_installs_lookup_start(state_manager):
        # TODO
        print('dcs_installs_lookup_start')

    @staticmethod
    def updater_finished(state_manager):
        sig_long_op_dialog.set_progress(100)
        sig_long_op_dialog.hide()
        MsgDialog.make('This is the latest version of EASI', 'Updater')

    @staticmethod
    def updater_started(state_manager):
        sig_long_op_dialog.show('Please wait...', 'Looking for a newer version of {}'.format(constants.APP_SHORT_NAME))
