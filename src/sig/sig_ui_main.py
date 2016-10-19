# coding=utf-8
from src.abstract.ui.main_ui_interface import AbstractMainUiInterface
from src.abstract.ui.main_ui_state import AbstractMainUiState
from .interface import interfaced_method, InterfacedSignal


class MainUiSig(InterfacedSignal, AbstractMainUiInterface):
    @interfaced_method
    def exit(self):
        pass

    @interfaced_method
    def show(self):
        pass

    @interfaced_method
    def hide(self):
        pass


class MainUiStatesSig(InterfacedSignal, AbstractMainUiState):
    @interfaced_method
    def show_msg(self, title, text: str, over_splash: bool = False):
        pass

    @interfaced_method
    def set_current_state(self, state: str):
        pass

    @interfaced_method
    def set_progress_title(self, value: str):
        pass

    @interfaced_method
    def set_progress_text(self, value: str):
        pass

    @interfaced_method
    def set_progress(self, value: int):
        pass

    @interfaced_method
    def add_progress(self, value: int):
        pass
