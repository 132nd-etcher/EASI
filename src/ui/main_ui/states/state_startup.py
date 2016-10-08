# coding=utf-8

from src.abstract.ui.main_ui_state import AbstractMainUiState

from src.sig import sig_splash, sig_msgbox


class UiStateStartup(AbstractMainUiState):
    def show_msg(self, title: str, text: str, over_splash: bool = False):
        if over_splash:
            sig_msgbox.show(title, text)

    def set_current_state(self, state: str):
        pass

    @staticmethod
    def set_progress_title(state_manager, value: str):
        sig_splash.show()
        sig_splash.set_progress_text(value)

    @staticmethod
    def set_progress_text(state_manager, value: str):
        pass

    @staticmethod
    def set_progress(state_manager, value: int):
        sig_splash.set_progress(value)

    @staticmethod
    def add_progress(state_manager, value: int):
        sig_splash.add_to_progress(value)
