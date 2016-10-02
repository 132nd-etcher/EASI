# coding=utf-8

import abc


class AbstractModFileMeta(metaclass=abc.ABCMeta):
    @property
    @abc.abstractproperty
    def name(self) -> str:
        """File's name"""

    @property
    @abc.abstractproperty
    def installs_to(self) -> str:
        """Target path of this file"""

    @property
    @abc.abstractproperty
    def size(self) -> int:
        """Size of the file in bytes"""


class AbstractModFileLocalMeta(AbstractModFileMeta, metaclass=abc.ABCMeta):
    @property
    @abc.abstractproperty
    def path(self) -> str:
        """Local filesystem path to this file"""


class AbstractModFileRemoteMeta(AbstractModFileMeta, metaclass=abc.ABCMeta):
    @property
    @abc.abstractproperty
    def download_link(self) -> str:
        """Link to download this file over HTTP"""

    @property
    @abc.abstractproperty
    def crc(self) -> str:
        """Cyclic redundancy check of the this file"""
