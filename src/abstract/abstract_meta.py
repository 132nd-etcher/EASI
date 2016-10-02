# coding=utf-8
import abc

from src.low.custom_path import Path
from .abstract_sentry import SentryContextInterface


class AbstractMeta(SentryContextInterface, metaclass=abc.ABCMeta):
    """
    Defines the interface for a class that holds Metadata.
    """

    @abc.abstractmethod
    def dump(self):
        """pass"""

    @abc.abstractmethod
    def load(self, data):
        """pass"""

    @abc.abstractmethod
    def read(self):
        """Reads meta from file"""

    @abc.abstractmethod
    def write(self):
        """Writes meta to file"""
