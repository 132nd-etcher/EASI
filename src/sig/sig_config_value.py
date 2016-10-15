# coding=utf-8
from src.sig.base_custom_signal import CustomSignal


class ConfigValueSig(CustomSignal):
    def value_changed(self, value):
        super(ConfigValueSig, self).send(value=value)
