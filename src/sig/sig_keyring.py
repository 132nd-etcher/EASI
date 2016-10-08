# coding=utf-8
from src.sig.base_custom_signal import CustomSignal


class KeyringSig(CustomSignal):
    def encrypt_changed(self, value: bool):
        super(KeyringSig, self).send(value=value)
