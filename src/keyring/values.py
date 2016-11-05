# coding=utf-8

from src.low.custom_logging import make_logger
from src.meta.meta_property import MetaProperty

logger = make_logger(__name__)


class KeyringValues:
    @MetaProperty(None, str)
    def gh_token(self, value: str) -> str:
        """"""

    @MetaProperty(None, str)
    def gh_username(self, value: str) -> str:
        """"""

    @MetaProperty(None, str)
    def gh_password(self, value: str) -> str:
        """"""

    @MetaProperty(None, str)
    def db_token(self, value: str) -> str:
        """"""
