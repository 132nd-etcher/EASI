# coding=utf-8


from src.cache.cache import Cache
from src.git.wrapper import Repository
from src.low.custom_logging import make_logger
from src.low.singleton import Singleton

logger = make_logger(__name__)


class OwnModRepo(Repository, metaclass=Singleton):
    def __init__(self, path):
        logger.debug('instantiating')
        Repository.__init__(self, path=path)
        if not self.path.exists():
            self.init()
