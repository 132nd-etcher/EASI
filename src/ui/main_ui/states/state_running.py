# coding=utf-8

from src.abstract.ui import AbstractMainUiState

from src.sig import sig_progress, sig_msgbox


class UiStateRunning(AbstractMainUiState):

    def set_current_state(self, state: str):
        pass

    @staticmethod
    def show_msg(state_manager, title: str, text: str, over_splash: bool = False):
        sig_msgbox.show(title, text)

    @staticmethod
    def set_progress_title(state_manager, value: str):
        sig_progress.show(title=value, text='')

    @staticmethod
    def set_progress_text(state_manager, value: str):
        sig_progress.set_progress_text(value)

    @staticmethod
    def set_progress(state_manager, value: int):
        sig_progress.set_progress(value)
        if value == 100:
            sig_progress.hide()

    @staticmethod
    def add_progress(state_manager, value: int):
        sig_progress.add_progress(value)
