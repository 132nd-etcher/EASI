# coding=utf-8

from src.sig.base_custom_signal import CustomSignal


class GHSig(CustomSignal):

    def __init__(self):
        CustomSignal.__init__(self)

    def not_connected(self):
        CustomSignal.send(self, status=0)

    def wrong_token(self):
        CustomSignal.send(self, status=-1)

    def connected(self, username):
        CustomSignal.send(self, status=1, username=username)


class DBSig(CustomSignal):

    def __init__(self):
        CustomSignal.__init__(self)

    def not_connected(self):
        CustomSignal.send(self, status=0)

    def wrong_token(self):
        CustomSignal.send(self, status=-1)

    def connected(self, username):
        CustomSignal.send(self, status=1, username=username)


