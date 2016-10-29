# coding=utf-8



import semver

from src.cache.cache import Cache
from src.git.own_mod_repo import OwnModRepo
from src.meta.meta import Meta
from src.meta.meta_property import MetaProperty
from src.mod.dcs_version import DCSVersion


class ModDraft(Meta):
    @property
    def meta_header(self):
        return 'EASI_MOD_DRAFT'

    def __init__(self, uuid):
        Meta.__init__(self, path=Cache().own_mods_folder.joinpath('{}.easi_mod_draft'.format(uuid)))
        self.uuid = uuid
        self.__repo = None

    @property
    def repo(self):
        if self.__repo is None:
            self.__repo = OwnModRepo(path=Cache().own_mods_folder.joinpath(self.name))
        return self.__repo

    @property
    def status(self):
        return 'draft'

    @property
    def has_changed(self):
        return self.repo.status != 0

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

    @MetaProperty(None, str)
    def version(self, value: str) -> str:
        try:
            semver.parse(value)
        except ValueError:
            raise

    @MetaProperty(None, str)
    def dcs_version(self, value: str) -> str:
        if not DCSVersion.is_valid(value):
            raise ValueError('not a valid DCS version: {}'.format(value))
