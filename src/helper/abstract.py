# coding=utf-8

import abc

from src.low.custom_path import Path


class AbstractHelper(metaclass=abc.ABCMeta):
    @property
    @abc.abstractproperty
    def helper_dir(self):
        """Root directory for all helpers"""

    @property
    def root_dir(self):
        return Path(self.helper_dir).joinpath(self.name)

    @property
    @abc.abstractproperty
    def download_link(self):
        """Link to download the helper"""

    @property
    @abc.abstractproperty
    def name(self):
        """Returns root directory for this helper"""

    @property
    @abc.abstractproperty
    def executable(self):
        """Path to this helper's executable file"""
