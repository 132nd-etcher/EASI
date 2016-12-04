# coding=utf-8

import typing
from collections import OrderedDict

from src.cache.cache import Cache
from src.low.custom_path import Path
from src.mod.mod_file import ModFile
from src.mod.mod_meta import ModMeta
from src.repo.irepo import IRepo
from src.low.custom_logging import make_logger
from src.sig import SigProgress
from src.low.fs_observer.fso import FSObserver, FSOFile, FSOEvent


logger = make_logger(__name__)


class Mod:
    def __init__(self, meta_path: Path, parent_meta_repo: IRepo):
        self.__meta = ModMeta(path=meta_path)
        self.__parent_meta_repo = parent_meta_repo

    def rename(self, new_name: str):
        logger.debug('renaming mod: {} -> {}'.format(self.meta.name, new_name))
        new_folder = self.local_folder.dirname().joinpath(new_name)
        logger.debug('moving files: {} -> {}'.format(self.local_folder, new_folder))
        self.local_folder.move(new_folder)
        old_meta_path = self.meta.path
        logger.debug('setting new meta path')
        self.meta.path = self.meta.path.dirname().joinpath(new_name)
        logger.debug('setting new name')
        self.meta.name = new_name
        logger.debug('writing updated meta')
        self.meta.write()
        logger.debug('removing old meta file')
        old_meta_path.remove()

    def commit_changes(self):
        SigProgress().show('Saving metadata...', '')
        files = list(self.local_files)
        current = 0
        d = OrderedDict()
        for mod_file in files:
            SigProgress().set_progress_text(mod_file.rel_path)
            d[str(mod_file.rel_path)] = mod_file.meta
            current += 1
            SigProgress().set_progress((current / len(files)) * 100)
        self.meta.files = d
        self.meta.write()

    @property
    def meta_repo(self):
        return self.__parent_meta_repo

    @property
    def local_folder(self) -> Path:
        local_folder = Path(Cache().mods_folder.joinpath(self.meta_repo.name).joinpath(self.meta.name))
        if not local_folder.exists():
            logger.debug('Mod {}: creating local folder: {}'.format(self.name, local_folder))
            local_folder.makedirs_p()
        return local_folder

    @property
    def meta(self) -> ModMeta:
        return self.__meta

    @property
    def has_new_files(self):
        return any({mod_file.is_new for mod_file in self.local_files})

    @property
    def has_modified_files(self):
        return any({mod_file.is_modified for mod_file in self.local_files})

    @property
    def has_deleted_files(self):
        return len(self.deleted_local_files) > 0

    @property
    def has_changed(self):
        return any({
            self.has_new_files,
            self.has_modified_files,
            self.has_deleted_files,
        })

    @property
    def local_files(self) -> typing.List[ModFile]:
        return [ModFile(self, file_path) for file_path in self.local_folder.listdir()]

    @property
    def deleted_local_files(self) -> typing.List[Path]:
        return [Path(local_file) for local_file in self.meta.files if not self.local_folder.joinpath(local_file) in Cache()]

    @property
    def name(self):
        return self.meta.name

    @property
    def uuid(self):
        return self.meta.uuid

    @property
    def author(self):
        return self.meta.author

    @property
    def category(self):
        return self.meta.category

    @property
    def dcs_version(self):
        return self.meta.dcs_version

    @property
    def description(self):
        return self.meta.description
