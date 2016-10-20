# coding=utf-8

from src.sig.interface import interfaced_method, InterfacedSignal
from .interface import TestingDialogInterface


class TestingDialogSig(InterfacedSignal, TestingDialogInterface):
    @interfaced_method
    def show(self):
        """"""


sig_testing_dialog = TestingDialogSig()


