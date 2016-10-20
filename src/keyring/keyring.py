# coding=utf-8
"""Manages credentials"""
from winreg import ConnectRegistry, HKEY_LOCAL_MACHINE, KEY_READ, KEY_WOW64_64KEY, OpenKey, QueryValueEx

from Crypto.Cipher import AES
from base64 import b64encode, b64decode

from src.cfg import config
from src.low import constants
from src.low.custom_logging import make_logger
from src.low.singleton import Singleton
from src.meta.meta import Meta
from src.sig import SignalReceiver, sig_cfg_keyring_encrypt
from .values import KeyringValues

logger = make_logger(__name__)


def pad(data):
    if len(data) % 32 == 0:
        return data
    if isinstance(data, str):
        return data + ((32 - len(data) % 32) * '@')
    else:
        raise TypeError
    # elif isinstance(data, bytes):
    #     return data + ((32 - len(data) % 32) * '@'.encode())


class Keyring(Meta, KeyringValues, metaclass=Singleton):
    """
    Manages known credentials
    """

    def __init__(self):
        Meta.__init__(self, path=constants.PATH_KEYRING_FILE, encrypted=config.encrypt_keyring)
        KeyringValues.__init__(self)
        self.rec = SignalReceiver(self)
        self.rec[sig_cfg_keyring_encrypt] = self.encrypt_keyring_setting_changed

    def encrypt_keyring_setting_changed(self, value: bool):
        self.encrypt = value
        self.write()

    def __setitem__(self, key, value, _write=True):
        """Immediately writes any change to file"""
        super(Keyring, self).__setitem__(key, value)
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
    pass

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
keyring = Keyring()
logger.info('keyring: initialized')
