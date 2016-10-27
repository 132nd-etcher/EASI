# coding=utf-8

import abc

from src.low.custom_path import Path


class AbstractHelperRunProfile:
    pass


class AbstractHelper:
    @abc.abstractmethod
    def run_profile(self, profile: AbstractHelperRunProfile):
        """Executes a profile with this helper"""

    @property
    @abc.abstractproperty
    def download_link(self):
        """Link to download the helper"""

    @property
    @abc.abstractproperty
    def is_installed(self):
        """"""

    @abc.abstractmethod
    def download_and_install(self, wait: bool = True):
        """"""

    @property
    @abc.abstractproperty
    def name(self):
        """"""

    @property
    @abc.abstractproperty
    def path(self) -> Path:
        """"""

    @path.setter
    @abc.abstractproperty
    def path(self, value: str or Path):
        """"""

    @property
    @abc.abstractproperty
    def folder(self):
        """"""
