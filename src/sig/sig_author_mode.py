# coding=utf-8
from src.sig.base_custom_signal import CustomSignal


class AuthorModeSig(CustomSignal):
    def mod_author_changed(self, value: bool):
        super(AuthorModeSig, self).send(value=value)
