# coding=utf-8

import abc
import typing

from .abstract_modfile_meta import AbstractModFileRemoteMeta


class AbstractModMetaRelations(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def depends(self, value) -> typing.List[str]:
        """List of mod IDs this mod depends on"""

    @abc.abstractmethod
    def recommends(self, value) -> typing.List[str]:
        """List of other mod this mod recommends"""

    @abc.abstractmethod
    def provides(self, value) -> typing.List[str]:
        """List of dependencies this mod provides"""

    @abc.abstractmethod
    def conflicts(self, value) -> typing.List[str]:
        """List of other mods this mod conflicts with"""


class AbstractModMetaLinks(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def homepage(self, value) -> str:
        """Default webpage for this mod (can be None)"""

    @abc.abstractmethod
    def help(self, value) -> str:
        """Link to this mod's help page (can be None)"""

    @abc.abstractmethod
    def repository(self, value) -> str:
        """Repository of the  mod (can be None)"""

    @abc.abstractmethod
    def issues(self, value) -> str:
        """Link to a webpage where issues with the mod can be reported (can be None)"""


class AbstractModMetaInformation(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def short_desc(self, value) -> str:
        """One liner describing the mod"""

    @abc.abstractmethod
    def long_description(self):
        """Full description of the mod"""

    @abc.abstractmethod
    def mod_type(self, value) -> str:
        """General category of the mod (skin, new vehicle, textures, ...)"""

    @abc.abstractmethod
    def release_status(self, value) -> str:
        """Current status of the mod [stable, testing, experimental]; defaults to stable"""

    @abc.abstractmethod
    def version(self, value) -> str:
        """Version of the mod"""


class AbstractModMetaBasics(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def author(self, value) -> str:
        """Name of the mod's creator"""

    @abc.abstractmethod
    def name(self, value) -> str:
        """Mod's name"""

    @abc.abstractmethod
    def meta_version(self, value) -> int:
        """Minimal version of EASI needed to read the metadata"""

    @abc.abstractmethod
    def identifier(self, value) -> str:
        """Unique ID of the mod"""

    @abc.abstractmethod
    def license(self, value) -> str:
        """License of the content"""


class AbstractModMetaDCSVersion(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def dcs_version(self, value) -> str:
        """Version of the DCS needed to use the mod (defaults to minimal, can be None"""

    @abc.abstractmethod
    def dcs_version_strict(self, value) -> bool:
        """Whether or not the DCS version must be strictly honored"""


class AbstractModMetaFileList(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def files(self, value) -> typing.List[AbstractModFileRemoteMeta]:
        """Files contained in this mod"""


class AbstractModMetaFull(
    AbstractModMetaBasics,
    AbstractModMetaRelations,
    AbstractModMetaLinks,
    AbstractModMetaInformation,
    AbstractModMetaDCSVersion,
    AbstractModMetaFileList,
    # metaclass=abc.ABCMeta
):
    def short_desc(self, value) -> str:
        pass

    def files(self, value) -> typing.List[AbstractModFileRemoteMeta]:
        pass

    def release_status(self, value) -> str:
        pass

    def identifier(self, value) -> str:
        pass

    def help(self, value) -> str:
        pass

    def recommends(self, value) -> typing.List[str]:
        pass

    def issues(self, value) -> str:
        pass

    def name(self, value) -> str:
        pass

    def version(self, value) -> str:
        pass

    def license(self, value) -> str:
        pass

    def dcs_version(self, value) -> str:
        pass

    def provides(self, value) -> typing.List[str]:
        pass

    def meta_version(self, value) -> int:
        pass

    def author(self, value) -> str:
        pass

    def dcs_version_strict(self, value) -> bool:
        pass

    def homepage(self, value) -> str:
        pass

    def long_description(self):
        pass

    def repository(self, value) -> str:
        pass

    def conflicts(self, value) -> typing.List[str]:
        pass

    def mod_type(self, value) -> str:
        pass

    def depends(self, value) -> typing.List[str]:
        pass
