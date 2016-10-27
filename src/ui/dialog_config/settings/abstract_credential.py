# coding=utf-8
import abc

from src.keyring.keyring import Keyring
from src.qt import QLabel
from .abstract import AbstractSetting


class AbstractCredentialSetting(AbstractSetting, metaclass=abc.ABCMeta):

    def __init__(self, dialog):
        AbstractSetting.__init__(self, dialog)
        self.auth_btn.clicked.connect(self.authenticate)

    @property
    def store_class(self):
        return Keyring

    @property
    def store_object(self):
        return Keyring()

    def status_changed(self, result):
        if result is None:
            self.status_label.setText('Not connected')
            self.status_label.setStyleSheet('QLabel { color : black; }')
        elif result is False:
            self.status_label.setText('Token was invalidated; please create a new one')
            self.status_label.setStyleSheet('QLabel { color : red; }')
        elif isinstance(result, str):
            self.status_label.setText('Connected as: {}'.format(result))
            self.status_label.setStyleSheet('QLabel { color : green; }')
        else:
            raise ValueError('unexpected result: {}'.format(result))

    @property
    @abc.abstractproperty
    def status_label(self) -> QLabel:
        """"""

    @property
    @abc.abstractproperty
    def auth_btn(self):
        """"""

    @abc.abstractmethod
    def authenticate(self):
        """"""

    def save_to_meta(self, value):
        setattr(self.store_object, self.value_name, value)

    def del_from_meta(self):
        delattr(self.store_object, self.value_name)
