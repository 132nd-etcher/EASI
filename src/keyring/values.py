# coding=utf-8

from src.low.custom_logging import make_logger
from src.meta.decorators import MetaProperty

logger = make_logger(__name__)


class KeyringValues:
    @MetaProperty(None, str)
    def gh_token(self, value: str) -> str:
        """Dictionary of Github tokens"""

    @MetaProperty(None, str)
    def db_token(self, value: str) -> str:
        """Dictionary of Github tokens"""
