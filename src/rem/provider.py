# coding=utf-8

import abc
from src.mod.mod import Mod


class HostingProvider:

    def __init__(self):
        pass

    def upload_mod_metadata(self, mod: Mod):
        pass

    @abc.abstractmethod
    def upload_mod_files(selfself, mod: Mod):
        """"""