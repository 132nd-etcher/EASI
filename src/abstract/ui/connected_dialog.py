# coding=utf-8

import abc

from src.qt import QDialog
from .base_dialog import AbstractBaseDialog
from .connected_qobject import AbstractConnectedQObject


class AbstractConnectedDialog(AbstractConnectedQObject, AbstractBaseDialog, metaclass=abc.ABCMeta):
    """
    Defines a dialog that is connected to the MainUi via a specific signal.

    Whenever this signal is sent, the first arg of the signal is assumed to be a valid method
    if the receiving AbstractConnectedDialog.
    """

    def __init__(self, sig, main_ui_obj_name, dialog: QDialog):
        from src.sig import CustomSignal, SignalReceiver
        if not isinstance(sig, CustomSignal):
            raise TypeError('expected CustomSignal, got: {}'.format(type(sig)))
        if not hasattr(dialog, 'label'):
            raise NotImplementedError('dialog {} is missing "label" object'.format(self.__class__.__name__))
        AbstractBaseDialog.__init__(self, dialog)
        AbstractConnectedQObject.__init__(self, sig, main_ui_obj_name, dialog)
        self.main_ui_obj_name = main_ui_obj_name
        self.receiver = SignalReceiver(self)
        self.receiver[sig] = self.on_sig
