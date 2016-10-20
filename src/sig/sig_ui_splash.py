# coding=utf-8
from src.abstract.progress_interface import ProgressInterface
from .interface import interfaced_method, InterfacedSignal


class SplashSig(InterfacedSignal, ProgressInterface):
    def set_current_text(self, value: str):
        pass

    def set_current_progress(self, value: int):
        pass

    def add_progress(self, value: int):
        pass

    def add_current_progress(self, value: int):
        pass

    def set_progress_title(self, value: str):
        pass

    def set_current_enabled(self, value: bool):
        pass

    @interfaced_method
    def hide(self):
        """"""

    @interfaced_method
    def set_progress_text(self, value: str):
        """"""

    @interfaced_method
    def get_progress(self):
        """"""

    @interfaced_method
    def get(self):
        """"""

    @interfaced_method
    def set_progress(self, value: int):
        """"""

    @interfaced_method
    def show(self, title: str = None, text: str = None, auto_close: bool = True):
        """"""

    @interfaced_method
    def add_to_progress(self, value: int):
        """"""

    @interfaced_method
    def current_progress(self):
        """"""
