# coding=utf-8

from src.abstract.ui import AbstractMainUiState

from src.sig import sig_long_op_dialog, sig_msgbox


class UiStateRunning(AbstractMainUiState):

    def set_current_state(self, state: str):
        pass

    @staticmethod
    def show_msg(state_manager, title: str, text: str, over_splash: bool = False):
        sig_msgbox.show(title, text)

    @staticmethod
    def set_progress_title(state_manager, value: str):
        sig_long_op_dialog.show(title=value, text='')

    @staticmethod
    def set_progress_text(state_manager, value: str):
        sig_long_op_dialog.set_progress_text(value)

    @staticmethod
    def set_progress(state_manager, value: int):
        sig_long_op_dialog.set_progress(value)
        if value == 100:
            sig_long_op_dialog.hide()

    @staticmethod
    def add_progress(state_manager, value: int):
        sig_long_op_dialog.add_progress(value)
