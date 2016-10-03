# coding=utf-8

from src.abstract.ui import AbstractMainUiState

from src.low import constants
from src.sig import sig_long_op_dialog
from src.ui.dialog_msg.dialog import MsgDialog


class UiStateRunning(AbstractMainUiState):
    @staticmethod
    def set_progress_text(state_manager, value: str):
        sig_long_op_dialog.set_text(value)

    @staticmethod
    def set_progress(state_manager, value: int):
        sig_long_op_dialog.set_progress(value)
        if value == 100:
            sig_long_op_dialog.hide()

    @staticmethod
    def add_progress(state_manager, value: int):
        sig_long_op_dialog.add_progress(value)