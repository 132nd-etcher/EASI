# coding=utf-8


import semver

from src.cache.cache import Cache
from src.git.own_mod_repo import OwnModRepo
from src.meta.meta import Meta
from src.meta.meta_property import MetaProperty


class ModDraft(Meta):
    @property
    def meta_header(self):
        return 'EASI_MOD_DRAFT'

    def __init__(self, uuid):
        Meta.__init__(self, path=Cache().own_mods_folder.joinpath(uuid))
        self.uuid = uuid
        self.__repo = None

    @property
    def repo(self):
        if self.__repo is None:
            self.__repo = OwnModRepo(path=Cache().own_mods_folder.joinpath(self.name))
        return self.__repo

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
