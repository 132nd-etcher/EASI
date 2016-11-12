# coding=utf-8
import semver

from src.meta.meta import Meta
from src.meta.meta_property import MetaProperty
from src.mod.dcs_version import DCSVersion


class ModMeta(Meta):
    @property
    def meta_header(self):
        return 'EASI_MOD'

    def write(self):
        if not self.name:
            raise ValueError('can\'t write mod metadata without a name')
        super(ModMeta, self).write()

    @MetaProperty('', str)
    def author(self, value: str) -> str:
        """"""

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

    @MetaProperty({}, dict)
    def files(self, value: dict) -> dict:
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
