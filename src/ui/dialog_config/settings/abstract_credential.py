# coding=utf-8
import abc

from src.sig import SignalReceiver, CustomSignal
from src.keyring.keyring import keyring, Keyring
from src.qt import QLabel
from .abstract import AbstractSetting


class AbstractCredentialSetting(AbstractSetting, metaclass=abc.ABCMeta):

    def __init__(self, dialog):
        AbstractSetting.__init__(self, dialog)
        self.receiver = SignalReceiver(self)
        self.receiver[self.token_changed_signal] = self.status_changed
        self.auth_btn.clicked.connect(self.authenticate)

    @property
    @abc.abstractproperty
    def token_changed_signal(self) -> CustomSignal:
        """"""

    @property
    def store_class(self):
        return Keyring

    @property
    def store_object(self):
        return keyring

    def status_changed(self, **kwargs):
        status = kwargs.get('status')
        if status == self.session_object.session_status['not_connected']:
            self.status_label.setText('Not connected')
            self.status_label.setStyleSheet('QLabel { color : black; }')
        if status == self.session_object.session_status['wrong_token']:
            self.status_label.setText('Token not accepted; please create a new one')
            self.status_label.setStyleSheet('QLabel { color : red; }')
        if status == self.session_object.session_status['connected']:
            self.status_label.setText('Connected as: {}'.format(kwargs.get('username')))
            self.status_label.setStyleSheet('QLabel { color : green; }')

    @property
    @abc.abstractproperty
    def status_label(self) -> QLabel:
        """"""

    @property
    @abc.abstractproperty
    def session_object(self):
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
