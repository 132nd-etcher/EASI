# coding=utf-8
from src.cache.cache_file import CacheFile
import humanize
from src.low.custom_path import Path


class ModFile:

    def __init__(self, mod, cache_file: CacheFile):
        self.cache_file = cache_file
        self.mod = mod

    @property
    def human_size(self):
        return humanize.naturalsize(self.cache_file.size, gnu=True)

    @property
    def rel_path(self):
        return Path(self.cache_file.abspath).relpath(self.mod.local_folder.abspath())