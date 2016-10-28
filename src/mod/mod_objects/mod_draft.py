# coding=utf-8


import semver

from src.cache.cache import Cache
from src.meta.meta import Meta
from src.meta.meta_property import MetaProperty


class ModDraft(Meta):
    @property
    def meta_header(self):
        return 'EASI_MOD_DRAFT'

    def __init__(self, uuid):
        Meta.__init__(self, path=Cache().get_mod_draft_path(uuid))
        self.uuid = uuid

    @MetaProperty(None, str)
    def uuid(self, value: str) -> str:
        """"""

    @MetaProperty('', str)
    def name(self, value: str) -> str:
        """"""

    @MetaProperty(None, str)
    def category(self, value: str) -> str:
        """"""

    @MetaProperty('', str)
    def description(self, value: str) -> str:
        """"""

    @MetaProperty('0.0.1', str)
    def version(self, value: str) -> str:
        try:
            semver.parse(value)
        except ValueError:
            raise
