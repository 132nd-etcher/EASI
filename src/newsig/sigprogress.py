# coding=utf-8

from src.abstract.progress_interface import ProgressInterface
from src.newsig.customsig import CustomSig


class SigProgress(ProgressInterface, metaclass=CustomSig):
    """
    App-wide Progress signal.
    Sent whenever a lengthy operation requires the set-up of some progress feedback.
    """

    def set_current_text(self, value: str):
        pass

    def add_progress(self, value: int):
        pass

    def set_progress_title(self, value: str):
        pass

    def set_progress_text(self, value: str):
        pass

    def show(self, title: str, text: str, auto_close: bool = True):
        pass

    def set_current_enabled(self, value: bool):
        pass

    def add_current_progress(self, value: int):
        pass

    def set_current_progress(self, value: int):
        pass

    def hide(self):
        pass

    def set_progress(self, value: int):
        pass
