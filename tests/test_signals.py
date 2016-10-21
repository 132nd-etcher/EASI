# coding=utf-8

import pytest
from unittest.mock import MagicMock

from hypothesis import given, example
from hypothesis import strategies as st

from src.sig import CustomSignal, SignalReceiver


class TestSignal:

    sig = None
    rec = None
    mock = None

    @pytest.fixture(autouse=True)
    def make_sig(self):
        self.sig = CustomSignal()
        self.rec = SignalReceiver(self)
        self.mock = MagicMock()
        self.rec.sig_callback = self.mock

    def test_basic_sig(self):
        i = 0

        def func(sender):
            assert sender, 'CustomSignal'
            nonlocal i
            i += 1

        # test double connection to the same func
        func2 = func
        self.sig.connect(func)
        self.sig.connect(func2)
        self.sig.send()
        assert i == 1

        # test multiple send
        def func3(_):
            nonlocal i
            i += 1

        self.sig.connect(func3)
        self.sig.send()
        assert i == 3

        # test disconnection
        self.sig.disconnect(func3)
        self.sig.send()
        assert i == 4

    def test_receiver_connect_disconnect(self):
        sig = CustomSignal()
        self.rec[sig] = self.mock
        sig.send()
        assert self.mock.call_count == 1
        del self.rec[sig]
        sig.send()
        assert self.mock.call_count == 1

    @given(s=st.one_of(st.text(), st.booleans(), st.integers(), st.floats()))
    @example(s='text')
    def test_receiver(self, s):
        sig = CustomSignal()
        rec = SignalReceiver(self)
        mock = MagicMock()
        rec[sig] = mock
        sig.send(t=s)
        mock.assert_called_once_with(t=s)
