# coding=utf-8
from src.abstract import AbstractMainUiInterface, AbstractMainUiState
from src.sig.interface import interfaced_method, InterfacedSignal


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
    def set_progress(self, value: int):
        pass

    @interfaced_method
    def add_progress(self, value: int):
        pass

    @interfaced_method
    def dcs_installs_lookup_finished(self):
        pass

    @interfaced_method
    def updater_finished(self):
        pass

    @interfaced_method
    def set_current_state(self, state: str):
        pass

    @interfaced_method
    def dcs_installs_lookup_start(self):
        pass

    @interfaced_method
    def updater_started(self):
        pass

    @interfaced_method
    def keyring_validation_finished(self):
        pass

    @interfaced_method
    def keyring_validation_start(self):
        pass
