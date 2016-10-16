# coding=utf-8

import os
import stat

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from src.low.custom_logging import make_logger
from src.low.custom_path import Path
from src.low.singleton import Singleton
from src.sig import SignalReceiver, sig_cfg_cache_path

logger = make_logger(__name__)


class CacheFile:
    def __init__(
            self,
            name: str,
            abspath: str,
            path: str,
            st):
        self.size = st.st_size
        self.atime = st.st_atime
        self.mtime = st.st_mtime
        self.ctime = st.st_ctime
        self.read_only = bool(stat.FILE_ATTRIBUTE_READONLY & st.st_file_attributes)
        self.hidden = bool(stat.FILE_ATTRIBUTE_HIDDEN & st.st_file_attributes)
        self.system = bool(stat.FILE_ATTRIBUTE_SYSTEM & st.st_file_attributes)
        self.archive = bool(stat.FILE_ATTRIBUTE_ARCHIVE & st.st_file_attributes)
        self.path = path
        self.abspath = abspath
        self.name = name
        self.__crc32 = None

    def __str__(self):
        return '\n\t\t'.join(['{}: {}'.format(k, getattr(self, k)) for k in self.__dict__])

    @property
    def crc32(self) -> str or None:
        return self.__crc32

    @crc32.setter
    def crc32(self, value: str):
        self.__crc32 = value

    def get_crc32(self):
        p = Path(self.abspath)
        self.__crc32 = p.crc32()


class Cache(FileSystemEventHandler, metaclass=Singleton):
    def __init__(self, path: str or Path = None):
        FileSystemEventHandler.__init__(self)
        if path is None:
            raise ValueError('first Cache instantiation must include path')
        if isinstance(path, str):
            path = Path(path)
        self.__path = path
        if not self.__path.exists():
            self.__path.makedirs_p()
        self.rec = SignalReceiver(self)
        self.rec[sig_cfg_cache_path] = self.cache_path_changed
        self.observer = Observer()
        self.observer.schedule(self, self.path, recursive=True)
        self.observer.start()
        self.meta = {}
        self.build()
        self.__is_building = True

    @property
    def is_building(self):
        return self.__is_building

    def on_created(self, event):
        if not event.is_directory:
            self.build(event.src_path)
            logger.debug('created: {}'.format(event.src_path))

    def on_modified(self, event):
        if not event.is_directory:
            self.build(event.src_path)
            logger.debug('modified: {}'.format(event.src_path))

    def on_moved(self, event):
        if not event.is_directory:
            del self.meta[event.src_path]
            self.build(event.dest_path)
            logger.debug('moved: {} -> {}'.format(event.src_path, event.dest_path))

    def on_deleted(self, event):
        if not event.is_directory:
            del self.meta[event.src_path]
            logger.debug('deleted: {}'.format(event.src_path))

    def build(self, rel_path: str = None):
        self.__is_building = True
        if rel_path is None:
            logger.info('re-building whole cache folder')
            self.meta = {}
            for root, folder, file in os.walk(self.path):
                for entry in os.scandir(root):
                    if entry.is_dir():
                        continue
                    path = entry.path
                    abspath = os.path.join(self.path.dirname(), path)
                    name = entry.name
                    meta = CacheFile(name, abspath, path, entry.stat())
                    self.meta[meta.path] = meta
            for v in self.meta.values():
                v.get_crc32()
        else:
            logger.debug('re-building cache for path: {}'.format(rel_path))
            path = rel_path
            abspath = os.path.abspath(rel_path)
            name = os.path.basename(rel_path)
            meta = CacheFile(name, abspath, path, os.stat(abspath))
            meta.get_crc32()
            self.meta[meta.path] = meta
        self.__is_building = False

    def cache_path_changed(self, value):
        self.path = value

    @property
    def path(self) -> Path:
        return self.__path

    @path.setter
    def path(self, value: str or Path):
        if isinstance(value, str):
            value = Path(value)
        self.__path = value

    def __getitem__(self, item) -> CacheFile:
        try:
            return self.meta.__getitem__(item)
        except KeyError:
            return self.meta.__getitem__(Path(item).relpath(self.path))

    def __contains__(self, item) -> bool:
        try:
            self.__getitem__(item)
            return True
        except KeyError:
            return False

    def __str__(self):
        out = ['cache object']
        for k, meta in self.meta.items():
            out.append('{}: {}'.format(k, self.meta[k]))
        return '\n\t'.join(out)

    def __iter__(self):
        for item in self.meta.values():
            yield item
