# coding=utf-8
"""Manages credentials"""
from base64 import b64encode, b64decode
from winreg import ConnectRegistry, HKEY_LOCAL_MACHINE, KEY_READ, KEY_WOW64_64KEY, OpenKey, QueryValueEx

from Crypto.Cipher import AES
from blinker import signal

from src.cfg import Config
from src.low import constants
from src.low.custom_logging import make_logger
from src.low.singleton import Singleton
from src.meta.meta import Meta
from .values import KeyringValues

logger = make_logger(__name__)


def pad(data):
    if len(data) % 32 == 0:
        return data
    if isinstance(data, str):
        return data + ((32 - len(data) % 32) * '@')
    else:
        raise TypeError


class Keyring(Meta, KeyringValues, metaclass=Singleton):
    """
    Manages known credentials
    """

    @property
    def meta_header(self):
        return 'EASI_KEYRING'

    def __init__(self):
        Meta.__init__(self, path=constants.PATH_KEYRING_FILE, encrypted=Config().encrypt_keyring)
        KeyringValues.__init__(self)

        def encrypt_keyring_value_changed(_, value):
            self.encrypt_keyring_setting_changed(value)

        signal('Config_encrypt_keyring_value_changed').connect(encrypt_keyring_value_changed, weak=False)

    def encrypt_keyring_setting_changed(self, value: bool):
        self.encrypt = value
        if self.data:
            self.write()

    def __setitem__(self, key, value, _write=True):
        """Immediately writes any change to file"""
        super(Keyring, self).__setitem__(key, value)
        if _write:
            self.write()

    def __delitem__(self, key, _write=True):
        """Immediately writes any change to file"""
        super(Keyring, self).__delitem__(key)
        if _write:
            self.write()

    def dump(self):
        if self.encrypt and constants.MACHINE_GUID:
            plain_data = super(Keyring, self).dump()
            cipher = AES.new(pad(constants.MACHINE_GUID[:32]))
            return b64encode(cipher.encrypt(pad(plain_data)))
        else:
            return super(Keyring, self).dump()

    def load(self, data):
        if self.encrypt and constants.MACHINE_GUID:
            cipher = AES.new(pad(constants.MACHINE_GUID[:32]))
            return super(Keyring, self).load(cipher.decrypt(b64decode(data)).decode('utf-8').rstrip('@'))
        else:
            return super(Keyring, self).load(data)


def init_keyring():
    logger.info('keyring: initializing')
    a_reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    try:
        with OpenKey(a_reg, r"SOFTWARE\Microsoft\Cryptography") as aKey:
            constants.MACHINE_GUID = QueryValueEx(aKey, "MachineGuid")[0]
    except FileNotFoundError:
        try:
            with OpenKey(a_reg, r"SOFTWARE\Microsoft\Cryptography", access=KEY_READ | KEY_WOW64_64KEY) as aKey:
                constants.MACHINE_GUID = QueryValueEx(aKey, "MachineGuid")[0]
        except FileNotFoundError:
            constants.MACHINE_UID = False
    Keyring()
    logger.info('keyring: initialized')
