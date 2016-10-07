# coding=utf-8
"""
Convenience module for storing/restoring per-user configuration values
"""
from src.low import constants
from src.low.custom_logging import make_logger
from src.low.singleton import Singleton
from src.meta import Meta
from .values import ConfigValues

logger = make_logger(__name__)



class Config(Meta, ConfigValues, metaclass=Singleton):
    def __init__(self, config_file=None):
        if config_file is None:
            config_file = constants.PATH_CONFIG_FILE
        Meta.__init__(self, path=config_file)
        ConfigValues.__init__(self)

    def __getitem__(self, key):
        """Mutes KeyError"""
        return self.get(key, None)

    def __setitem__(self, key, value, _write=True):
        """Immediately writes any change to file"""
        super(Config, self).__setitem__(key, value)
        if _write:
            self.write()

    def write(self):
        if constants.TESTING:
            return
        super(Config, self).write()


logger.info('config: initializing')
config = Config()
logger.info('config: initialized')
