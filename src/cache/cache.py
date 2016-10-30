# coding=utf-8

import abc
import os
import stat

from blinker import signal
from blinker_herald import emit, signals
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from src.low.custom_logging import make_logger
from src.low.custom_path import Path
from src.low.singleton import Singleton
from src.rem.gh.gh_session import GHSession

logger = make_logger(__name__)


class CacheEvent:
    """
    Represents an event sent by the Cache when the watched filesystem is changed
    """

    def __init__(self, event_type: str, src: str, dst: str = None):
        self.event_type = event_type
        self.src = Path(src)
        self.dst = Path(dst) if dst else dst

    def __str__(self):
        return '{}: {}'.format(
            self.event_type, self.src if self.dst is None else '{} -> {}'.format(
                self.src, self.dst))


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
        if self.__crc32 is None:
            self.get_crc32()
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

        def on_path_changed(_, value):
            self.path = value
            self.cache_build()

        signal('Config_cache_path_value_changed').connect(on_path_changed, weak=False)
        self.observer = Observer()
        self.observer.schedule(self, self.path, recursive=True)
        self.observer.start()
        self.meta = {}
        self.__is_building = False
        self.cache_build()

    @property
    def meta_repos_folder(self) -> Path:
        p = Path(self.path.joinpath('meta_repos'))
        if not p.exists():
            p.makedirs()
        return p

    @property
    def mods_folder(self) -> Path:
        p = Path(self.path.joinpath('mods'))
        if not p.exists():
            p.makedirs()
        return p

    @property
    def own_mods_folder(self) -> Path:
        p = Path(self.path.joinpath('own_mods'))
        if not p.exists():
            p.makedirs()
        return p

    @property
    def own_meta_repo_folder(self):
        if not GHSession().has_valid_token:
            raise RuntimeError('GHSession has no valid token')
        p = Path(self.path.joinpath('own_meta_repo').joinpath(GHSession().user.login))
        if not p.exists():
            p.makedirs()
        return p

    @property
    def is_building(self):
        return self.__is_building

    @staticmethod
    def __filter_event(event):
        if event.is_directory:
            return False
        if '\\.git' in event.src_path:
            return False
        return True

    def on_created(self, event):
        if self.__filter_event(event):
            logger.debug('created: {}'.format(event.src_path))
            self.cache_build(event.src_path)
            self.cache_changed_event(CacheEvent('created', event.src_path))

    def on_modified(self, event):
        if self.__filter_event(event):
            logger.debug('modified: {}'.format(event.src_path))
            self.cache_build(event.src_path)
            self.cache_changed_event(CacheEvent('modified', event.src_path))

    def on_moved(self, event):
        if self.__filter_event(event):
            logger.debug('moved: {} -> {}'.format(event.src_path, event.dest_path))
            del self.meta[event.src_path]
            self.cache_build(event.dest_path)
            self.cache_changed_event(CacheEvent('moved', event.src_path, event.dest_path))

    def on_deleted(self, event):
        if self.__filter_event(event):
            logger.debug('deleted: {}'.format(event.src_path))
            try:
                del self.meta[event.src_path]
            except KeyError:
                pass
            self.cache_changed_event(CacheEvent('deleted', event.src_path))

    @emit(sender='Cache', post_result_name='event')
    def cache_changed_event(self, event: CacheEvent):
        return event

    @emit(sender='Cache', capture_result=False)
    def cache_build(self, rel_path: str = None):
        self.__is_building = True
        try:
            if rel_path is None:
                logger.info('re-building whole cache folder')
                self.meta = {}
                for root, folder, _ in os.walk(self.path):
                    if '\\.git' in root:
                        continue
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
                if '\\.git' in rel_path:
                    pass
                else:
                    logger.debug('re-building cache for path: {}'.format(rel_path))
                    path = rel_path
                    abspath = os.path.abspath(rel_path)
                    name = os.path.basename(rel_path)
                    try:
                        meta = CacheFile(name, abspath, path, os.stat(abspath))
                    except FileNotFoundError:
                        logger.debug('file was deleted, canceling')
                        return
                    meta.get_crc32()
                    self.meta[meta.path] = meta
        finally:
            self.__is_building = False

    @property
    def path(self) -> Path:
        return self.__path

    @path.setter
    def path(self, value: str or Path):
        if isinstance(value, str):
            value = Path(value)
        self.__path = value

    def __len__(self):
        return len(self.meta)

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
        for k in self.meta.keys():
            out.append('{}: {}'.format(k, self.meta[k]))
        return '\n\t'.join(out)

    def __iter__(self):
        for item in self.meta.values():
            yield item


class CacheEventCatcher:
    @staticmethod
    @abc.abstractstaticmethod
    @signals.post_cache_changed_event.connect
    def on_cache_changed_event_signal(sender: str, signal_emitter: Cache, event: CacheEvent):
        pass


def init_cache():
    logger.info('initializing cache')
    from src.cfg import Config
    p = Path(Config().cache_path)
    logger.debug('cache will be in: {}'.format(p.abspath()))
    if not p.exists():
        logger.debug('directory does not exist, creating')
        p.makedirs()
    Cache(p)
    logger.info('cache initialized')
