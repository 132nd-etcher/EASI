# coding=utf-8


import os

from src.cache.cache import Cache
from src.git.wrapper import Repository
from src.low.custom_path import Path
from src.mod.mod_meta import ModMeta

class Mod:
    def __init__(self, meta_path: Path, parent_meta_repo, new_mod_name: str or None = None):
        self.__meta = ModMeta(path=meta_path)
        self.__repo = Repository(path=Path(Cache().own_mods_folder.joinpath(new_mod_name or self.meta.name)))
        self.__parent = parent_meta_repo

    @property
    def meta_repo(self):
        return self.__parent

    @property
    def repo(self) -> Repository:
        return self.__repo

    @property
    def meta(self) -> ModMeta:
        return self.__meta

    @property
    def has_changed(self):
        return len(self.repo.status) > 0

    @property
    def local_files(self):
        for root, folders, files in os.walk(self.repo.path, topdown=True):
            folders[:] = [d for d in folders if d not in ['.git']]
            for file in files:
                yield os.path.join(root, file)
