# coding=utf-8

from src.low.custom_logging import make_logger
from src.meta import MetaPropertyWithDefault

logger = make_logger(__name__)


class KeyringValues:
    @MetaPropertyWithDefault(None, str)
    def gh_token(self, value: str) -> str:
        """Dictionary of Github tokens"""

    @MetaPropertyWithDefault(None, str)
    def db_token(self, value: str) -> str:
        """Dictionary of Github tokens"""
