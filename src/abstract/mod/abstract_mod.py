# coding=utf-8

import abc

from src.abstract.mod.abstract_mod_meta import AbstractModMetaFull


class AbstractMod(metaclass=abc.ABCMeta):
    @property
    @abc.abstractproperty
    def meta(self) -> AbstractModMetaFull:
        """Meta data of this mod"""
