# coding=utf-8

from src.low.custom_logging import make_logger
from src.meta import meta_property_with_default

logger = make_logger(__name__)


class KeyringValues:
    @meta_property_with_default(None, str)
    def gh_token(self, value: str) -> str:
        """Dictionary of Github tokens"""

    @meta_property_with_default(None, str)
    def db_token(self, value: str) -> str:
        """Dictionary of Github tokens"""
