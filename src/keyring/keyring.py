# coding=utf-8
"""Manages credentials"""

from src.low import constants
from src.low.custom_logging import make_logger
from src.low.singleton import Singleton
from src.meta import Meta
from .values import KeyringValues

logger = make_logger(__name__)


class Keyring(Meta, KeyringValues, metaclass=Singleton):
    """
    Manages known credentials
    """

    def __init__(self):
        Meta.__init__(self, path=constants.PATH_KEYRING_FILE)
        KeyringValues.__init__(self)

    def __setitem__(self, key, value, _write=True):
        """Immediately writes any change to file"""
        super(Keyring, self).__setitem__(key, value)
        if _write:
            self.write()


logger.info('keyring: initializing')
keyring = Keyring()
logger.info('keyring: initialized')
