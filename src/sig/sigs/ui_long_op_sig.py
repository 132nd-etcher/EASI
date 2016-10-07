# coding=utf-8
from src.abstract import AbstractLongOp
from ..interface import interfaced_method, InterfacedSignal


class AbstractLongOpDialogSig(InterfacedSignal, AbstractLongOp):
    @interfaced_method
    def set_text(self, value: str):
        pass

    @interfaced_method
    def add_progress(self, value: int):
        """"""

    @interfaced_method
    def set_progress(self, value: int):
        """"""

    @interfaced_method
    def show(self, title: str, text: str):
        """"""

    @interfaced_method
    def hide(self):
        """"""

    @interfaced_method
    def add_current_progress(self, value: int):
        """"""

    @interfaced_method
    def set_current_progress(self, value: int):
        """"""

    @interfaced_method
    def set_current_text(self, value: str):
        """"""

    @interfaced_method
    def set_current_enabled(self, value: bool):
        """Shows or hides the "current" bar and label"""
