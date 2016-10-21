# coding=utf-8

import typing

from src.abstract.mod.abstract_mod_meta import AbstractModMetaFull, AbstractModFileRemoteMeta
from src.meta.decorators import MetaProperty
from src.meta.meta import Meta


class ModMeta(Meta, AbstractModMetaFull):
    def __init__(self):
        Meta.__init__(self, '')

    @MetaProperty(None, str)
    def depends(self, value) -> typing.List[str]:
        pass

    @MetaProperty(None, list)
    def conflicts(self, value) -> typing.List[str]:
        pass

    @MetaProperty(None, str)
    def license(self, value) -> str:
        pass

    @MetaProperty(None, str)
    def identifier(self, value) -> str:
        pass

    @MetaProperty(None, str)
    def help(self, value) -> str:
        pass

    @MetaProperty(None, str)
    def name(self, value) -> str:
        pass

    @MetaProperty(None, str)
    def dcs_version(self, value) -> str:
        pass

    @MetaProperty(None, str)
    def short_desc(self, value) -> str:
        pass

    @MetaProperty(None, list)
    def recommends(self, value) -> typing.List[str]:
        pass

    @MetaProperty(None, bool)
    def dcs_version_strict(self, value) -> bool:
        pass

    @MetaProperty(None, str)
    def homepage(self, value) -> str:
        pass

    @MetaProperty(None, str)
    def release_status(self, value) -> str:
        pass

    @MetaProperty(None, list)
    def files(self, value) -> typing.List[AbstractModFileRemoteMeta]:
        pass

    @MetaProperty(None, str)
    def version(self, value) -> str:
        pass

    @MetaProperty(None, str)
    def repository(self, value) -> str:
        pass

    @MetaProperty(None, str)
    def issues(self, value) -> str:
        pass

    @MetaProperty(None, str)
    def long_description(self):
        pass

    @MetaProperty(None, str)
    def mod_type(self, value) -> str:
        pass

    @MetaProperty(None, int)
    def meta_version(self, value) -> int:
        pass

    @MetaProperty(None, list)
    def provides(self, value) -> typing.List[str]:
        pass

    @MetaProperty(None, str)
    def author(self, value) -> str:
        pass
