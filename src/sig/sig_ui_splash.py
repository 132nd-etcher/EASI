# coding=utf-8
from src.abstract.ui.splash import AbstractSplash
from .interface import interfaced_method, InterfacedSignal


class SplashSig(InterfacedSignal, AbstractSplash):
    @interfaced_method
    def kill(self):
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
    def show(self):
        """"""

    @interfaced_method
    def add_to_progress(self, value: int):
        """"""

    @interfaced_method
    def current_progress(self):
        """"""
