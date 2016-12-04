# coding=utf-8

import abc
import inspect
import sys
from src.cache.cache_file import CacheFile
import humanize
from src.low.custom_path import Path
from collections import OrderedDict
import datetime


class ModFileAction:
    @property
    @abc.abstractproperty
    def action_name(self) -> str:
        """"""


class ModFileInstall(ModFileAction):
    @property
    def action_name(self) -> str:
        return 'install'


class ModFileRemove(ModFileAction):
    @property
    def action_name(self) -> str:
        return 'remove'


class ModFileAppend(ModFileAction):
    @property
    def action_name(self) -> str:
        return 'append'


class ModFile:

    def __init__(self, mod, cache_file: CacheFile):
        self.cache_file = cache_file
        self.mod = mod
        self.__meta = OrderedDict(self.mod.meta.files.get(str(self.rel_path), OrderedDict()))
        self.__meta.update(
            OrderedDict(
                size=self.cache_file.size,
                rel_path=str(self.rel_path),
                crc32=self.cache_file.crc32,
            )
        )
        if 'action' not in self.__meta:
            self.__meta['action'] = 'install'

    @property
    def meta(self) -> OrderedDict:
        return self.__meta

    @property
    def last_changed(self):
        return humanize.naturaltime(datetime.datetime.fromtimestamp(self.cache_file.mtime))

    @property
    def human_size(self):
        return humanize.naturalsize(self.cache_file.size, gnu=True)

    @property
    def rel_path(self) -> Path:
        return Path(self.cache_file.abspath).relpath(self.mod.local_folder.abspath())

    @property
    def abspath(self):
        return Path(self.cache_file.abspath)

    @property
    def crc32(self):
        return self.cache_file.crc32

    @property
    def action(self) -> str:
        return self.__meta.get('action', 'install')

    @action.setter
    def action(self, value: str):
        if value not in available_actions():
            raise ValueError('unknown action: {}'.format(value))
        self.__meta['action'] = value


def available_actions():
    for cls_name, cls in inspect.getmembers(sys.modules[__name__], inspect.isclass):
        if issubclass(cls, ModFileAction) and not cls_name == 'ModFileAction':
            yield cls().action_name
