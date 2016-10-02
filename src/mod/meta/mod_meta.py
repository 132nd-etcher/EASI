# coding=utf-8

import typing

from src.abstract import AbstractModMetaFull, AbstractModFileRemoteMeta
from src.low.meta import Meta, meta_property_with_default


class ModMeta(Meta, AbstractModMetaFull):
    def __init__(self):
        Meta.__init__(self)

    @meta_property_with_default(None, str)
    def depends(self, value) -> typing.List[str]:
        pass

    @meta_property_with_default(None, list)
    def conflicts(self, value) -> typing.List[str]:
        pass

    @meta_property_with_default(None, str)
    def license(self, value) -> str:
        pass

    @meta_property_with_default(None, str)
    def identifier(self, value) -> str:
        pass

    @meta_property_with_default(None, str)
    def help(self, value) -> str:
        pass

    @meta_property_with_default(None, str)
    def name(self, value) -> str:
        pass

    @meta_property_with_default(None, str)
    def dcs_version(self, value) -> str:
        pass

    @meta_property_with_default(None, str)
    def short_desc(self, value) -> str:
        pass

    @meta_property_with_default(None, list)
    def recommends(self, value) -> typing.List[str]:
        pass

    @meta_property_with_default(None, bool)
    def dcs_version_strict(self, value) -> bool:
        pass

    @meta_property_with_default(None, str)
    def homepage(self, value) -> str:
        pass

    @meta_property_with_default(None, str)
    def release_status(self, value) -> str:
        pass

    @meta_property_with_default(None, list)
    def files(self, value) -> typing.List[AbstractModFileRemoteMeta]:
        pass

    @meta_property_with_default(None, str)
    def version(self, value) -> str:
        pass

    @meta_property_with_default(None, str)
    def repository(self, value) -> str:
        pass

    @meta_property_with_default(None, str)
    def issues(self, value) -> str:
        pass

    @meta_property_with_default(None, str)
    def long_description(self):
        pass

    @meta_property_with_default(None, str)
    def mod_type(self, value) -> str:
        pass

    @meta_property_with_default(None, int)
    def meta_version(self, value) -> int:
        pass

    @meta_property_with_default(None, list)
    def provides(self, value) -> typing.List[str]:
        pass

    @meta_property_with_default(None, str)
    def author(self, value) -> str:
        pass
