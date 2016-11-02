# coding=utf-8


import os

from src.cache.cache import Cache
from src.git.wrapper import Repository
from src.low.custom_path import Path
from src.mod.mod_meta import ModMeta
from src.mod.mod_repo import OwnModRepo


class Mod:
    def __init__(self, meta_path, delay_repo=False):
        self.__meta = ModMeta(path=meta_path)
        if not delay_repo:
            self.__repo = OwnModRepo(path=Path(Cache().own_mods_folder.joinpath(self.meta.name)))
        else:
            self.__repo = None

    @property
    def repo_path(self) -> Path:
        return self.repo.path

    @property
    def repo(self) -> Repository:
        if self.__repo is None:
            if self.meta.name == '':
                raise ValueError('cannot create repo without a valid mod name')
            self.__repo = OwnModRepo(path=Path(Cache().own_mods_folder.joinpath(self.meta.name)))
        return self.__repo

    @property
    def meta_path(self) -> Path:
        return self.meta.path

    @property
    def meta(self) -> ModMeta:
        return self.__meta

    @property
    def has_changed(self):
        return len(self.repo.status) > 0

    @property
    def local_files(self):
        for root, folders, files in os.walk(self.repo_path, topdown=True):
            folders[:] = [d for d in folders if d not in ['.git']]
            for file in files:
                yield os.path.join(root, file)
