# coding=utf-8


from src.cache.cache import Cache
from src.low.custom_path import Path
from src.mod.mod_file import ModFile
from src.mod.mod_meta import ModMeta


class Mod:
    def __init__(self, meta_path: Path, parent_meta_repo):
        self.__meta = ModMeta(path=meta_path)
        self.__parent_meta_repo = parent_meta_repo
        if not self.local_folder.exists():
            self.local_folder.makedirs_p()

    def rename(self, new_name: str):
        print('renaming: ', new_name)
        print(self.local_folder, ' -> ', self.local_folder.dirname().joinpath(new_name))
        return
        self.local_folder.move(Path(Cache().mods_folder.joinpath(self.meta_repo.name).joinpath(new_name)))
        self.meta.path = self.meta.path.dirname().joinpath(new_name)
        self.meta.name = new_name
        self.meta.write()

    @property
    def meta_repo(self):
        return self.__parent_meta_repo

    @property
    def local_folder(self) -> Path:
        return Path(Cache().mods_folder.joinpath(self.meta_repo.name).joinpath(self.meta.name))

    @property
    def meta(self) -> ModMeta:
        return self.__meta

    @property
    def has_changed(self):
        for mod_file in set(self.local_files):
            if mod_file.has_changed:
                return True
        return False

    @property
    def local_files(self):
        return [ModFile(self, cache_file) for cache_file in Cache().files_in(self.local_folder) if not cache_file.isdir]

    @property
    def deleted_local_files(self):
        return [local_file for local_file in self.meta.files if not self.local_folder.joinpath(local_file) in Cache()]

    @property
    def local_mod_files(self) -> dict:
        return {mod_file.abspath: mod_file for mod_file in self.local_files}
