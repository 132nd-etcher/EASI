# coding=utf-8

import abc

from .abstract_modfile_meta import AbstractModFileMeta


class AbstractModFile(metaclass=abc.ABCMeta):
    @property
    @abc.abstractproperty
    def meta(self) -> AbstractModFileMeta:
        """Meta data of this mod file"""
