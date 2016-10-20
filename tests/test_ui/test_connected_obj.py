# coding=utf-8

import pytest

import src.ui.base.with_signal
from src.ui.base.with_signal import WithSignal

from src.sig import CustomSignal

sig = CustomSignal()


class C(WithSignal):
    pass


def test_mock_main_ui_not_initialized():
    src.ui.base.with_signal.main_ui = None
    with pytest.raises(RuntimeError):
        C(sig, 'some_obj')


def test_connected_object(mocker, mock_main_ui):
    c = C(sig, 'some_obj')
    c.some_func = mocker.MagicMock()
    sig.send(op='some_func')
    mock_main_ui.sig_proc.do.assert_called_with('some_obj', 'some_func')


def test_missing_op(mock_main_ui):
    assert hasattr(mock_main_ui, 'some_obj')
    with pytest.raises(AttributeError):
        C(sig, 'some_obj')
        sig.send(op='missing_op')


def test_missing_obj(mock_main_ui):
    assert hasattr(mock_main_ui, 'some_obj')
    with pytest.raises(AttributeError):
        C(sig, 'missing_obj')
        sig.send(op='some_func')


def test_not_a_signal(mock_main_ui):
    assert hasattr(mock_main_ui, 'some_obj')
    with pytest.raises(TypeError):
        C('not_a_sig', 'some_obj')
        sig.send(op='some_func')
