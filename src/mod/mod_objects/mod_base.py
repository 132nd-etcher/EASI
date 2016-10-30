# coding=utf-8

import abc

import semver

from src.cache.cache import Cache
from src.git.own_mod_repo import OwnModRepo
from src.meta.meta_property import MetaProperty
from src.mod.dcs_version import DCSVersion
from src.low.custom_path import Path


class BaseMod:
    def __init__(self, uuid):
        self.uuid = uuid
        self._repo = None

    @property
    def repo_path(self) -> Path:
        return Path(Cache().own_mods_folder.joinpath(self.name))

    @property
    def repo(self):
        if self._repo is None:
            self._repo = OwnModRepo(path=self.repo_path)
        return self._repo

    @abc.abstractclassmethod
    def trash(self):
        """"""

    @abc.abstractclassmethod
    def write(self):
        """"""

    @property
    @abc.abstractproperty
    def status(self):
        """"""

    @property
    def has_changed(self):
        return len(self.repo.status) > 0

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
