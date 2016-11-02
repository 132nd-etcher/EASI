# coding=utf-8
import semver

from src.meta.meta import Meta
from src.meta.meta_property import MetaProperty
from src.mod.dcs_version import DCSVersion


class ModMeta(Meta):
    @property
    def meta_header(self):
        return 'EASI_MOD'

    @MetaProperty('', str)
    def status(self, value: str) -> str:
        """"""

    @MetaProperty('', str)
    def uuid(self, value: str) -> str:
        """"""

    @MetaProperty('', str)
    def name(self, value: str) -> str:
        """"""

    @MetaProperty('', str)
    def category(self, value: str) -> str:
        """"""

    @MetaProperty('', str)
    def description(self, value: str) -> str:
        """"""

    @MetaProperty('', str)
    def version(self, value: str) -> str:
        try:
            semver.parse(value)
        except ValueError:
            raise

    @MetaProperty('', str)
    def dcs_version(self, value: str) -> str:
        if not DCSVersion.is_valid(value):
            raise ValueError('not a valid DCS version: {}'.format(value))

    def write(self):
        # for attr in ['name', 'version', 'category', 'dcs_version']:
        #     if getattr(self, attr, '') == '':
        #         raise ValueError('invalid mod {}: {}'.format(attr, getattr(self, attr, '')))
        # try:
        #     semver.parse(self.version)
        # except ValueError:
        #     raise ValueError('invalid mod version: {}'.format(self.version))
        if not self.name:
            raise ValueError('can\'t write mod metadata without a name')
        super(ModMeta, self).write()
