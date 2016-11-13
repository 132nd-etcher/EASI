# coding=utf-8


from src.cache.cache import Cache
from src.low.custom_path import Path
from src.mod.mod_file import ModFile
from src.mod.mod_meta import ModMeta


class Mod:
    def __init__(self, meta_path: Path, parent_meta_repo):
        self.__meta = ModMeta(path=meta_path)
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
        for mod_file in set(self.local_files):
            if mod_file.rel_path not in self.meta.files:
                return True
            else:
                if mod_file.meta != self.meta.files[mod_file.rel_path]:
                    return True
        return False

    @property
    def local_files(self):
        for cache_file in Cache().files_in(self.local_folder):
            if not cache_file.isdir:
                yield ModFile(self, cache_file)
