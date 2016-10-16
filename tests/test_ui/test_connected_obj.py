# coding=utf-8

import pytest

import src.abstract.ui.connected_object
from src.abstract.ui.connected_object import AbstractConnectedObject
from src.sig import CustomSignal

sig = CustomSignal()


class C(AbstractConnectedObject):
    pass


def test_main_ui_not_initialized():
    src.abstract.ui.connected_object.main_ui = None
    with pytest.raises(RuntimeError):
        C(sig, 'some_obj')


def test_connected_object(mocker, main_ui):
    c = C(sig, 'some_obj')
    c.some_func = mocker.MagicMock()
    sig.send(op='some_func')
    main_ui.sig_proc.do.assert_called_with('some_obj', 'some_func')


def test_missing_op(main_ui):
    with pytest.raises(AttributeError):
        C(sig, 'some_obj')
        sig.send(op='missing_op')


def test_missing_obj(main_ui):
    with pytest.raises(AttributeError):
        C(sig, 'missing_obj')
        sig.send(op='some_func')


def test_not_a_signal(main_ui):
    with pytest.raises(TypeError):
        C('not_a_sig', 'some_obj')
        sig.send(op='some_func')
