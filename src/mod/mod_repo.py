# coding=utf-8
from src.git.wrapper import Repository
from src.low.custom_logging import make_logger

logger = make_logger(__name__)


class OwnModRepo(Repository):
    def __init__(self, path):
        logger.debug('creating mod repo in {}'.format(path))
        Repository.__init__(self, path=path)
        if not self.path.exists():
            self.init()
