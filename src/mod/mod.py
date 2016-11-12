# coding=utf-8


import os

from src.cache.cache import Cache
from src.git.wrapper import Repository
from src.low.custom_path import Path
from src.mod.mod_meta import ModMeta
from src.mod.mod_file import ModFile


class Mod:
    def __init__(self, meta_path: Path, parent_meta_repo, new_mod_name: str or None = None):
        self.__meta = ModMeta(path=meta_path)
        # self.__repo = Repository(path=Path(Cache().own_mods_folder.joinpath(new_mod_name or self.meta.name)))
        self.__parent = parent_meta_repo
        if not self.local_folder.exists():
            self.local_folder.makedirs_p()

    @property
    def meta_repo(self):
        return self.__parent

    @property
    def local_folder(self) -> Path:
        return Path(Cache().mods_folder.joinpath(self.meta_repo.name).joinpath(self.meta.name))

    @property
    def meta(self) -> ModMeta:
        return self.__meta

    @property
    def has_changed(self):
        return False  #FIXME
        # return len(self.repo.status) > 0

    @property
    def local_files(self):
        for cache_file in Cache().files_in(self.local_folder):
            yield ModFile(self, cache_file)
