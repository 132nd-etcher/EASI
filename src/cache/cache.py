# coding=utf-8

import abc
import os

from blinker import signal
from blinker_herald import emit, signals
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from src.cache.cache_event import CacheEvent
from src.cache.cache_file import CacheFile
from src.low.custom_logging import make_logger
from src.low.custom_path import Path, create_temp_file, create_temp_dir
from src.low.singleton import Singleton
from src.rem.gh.gh_session import GHSession

from src.sig import SigProgress

logger = make_logger(__name__)


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
            logger.warning('changing cache path to: {}'.format(value))
            self.path = value
            self.cache_build()

        signal('Config_cache_path_value_changed').connect(on_path_changed, weak=False)
        self.observer = Observer()
        self.observer.schedule(self, self.path, recursive=True)
        self.observer.start()
        self.meta = {}
        self.__is_building = False
        self.cache_build()

    def files_in(self, rel_path):
        for x in self:
            if x.abspath.startswith(rel_path):
                yield x

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
        if not GHSession().user:
            raise FileNotFoundError('GHSession has no valid token')
        p = Path(self.meta_repos_folder.joinpath(GHSession().user))
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
        if '\\.git\\' in event.src_path:
            return False
        return True

    def on_created(self, event):
        if self.__filter_event(event):
            logger.debug('{}'.format(event.src_path))
            self.cache_build(event.src_path)
            self.cache_changed_event(CacheEvent('created', event.src_path))

    def on_modified(self, event):
        if self.__filter_event(event):
            logger.debug('{}'.format(event.src_path))
            self.cache_build(event.src_path)
            self.cache_changed_event(CacheEvent('modified', event.src_path))

    def on_moved(self, event):
        if self.__filter_event(event):
            logger.debug('{} -> {}'.format(event.src_path, event.dest_path))
            try:
                del self.meta[event.src_path]
            except KeyError:
                # Src wasn't in the cache anyway
                pass
            self.cache_build(event.dest_path)
            self.cache_changed_event(CacheEvent('moved', event.src_path, event.dest_path))

    def on_deleted(self, event):
        if self.__filter_event(event):
            logger.debug('{}'.format(event.src_path))
            try:
                del self.meta[event.src_path]
            except KeyError:
                logger.debug('not in cache, skipping')
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
                SigProgress().set_progress(0)
                SigProgress().set_progress_text('Building local cache')
                self.meta = {}
                total = 0
                count = 0
                for root, folders, _ in os.walk(self.path, topdown=True):
                    folders[:] = [d for d in folders if d not in ['.git']]
                    folders[:] = [d for d in folders if d not in ['temp']]
                    for _ in os.scandir(root):
                        total += 1
                for root, folders, _ in os.walk(self.path, topdown=True):
                    folders[:] = [d for d in folders if d not in ['.git']]
                    folders[:] = [d for d in folders if d not in ['temp']]
                    for entry in os.scandir(root):
                        if entry.is_dir():
                            continue
                        path = entry.path
                        abspath = os.path.join(self.path.dirname(), path)
                        name = entry.name
                        isdir = os.path.isdir(abspath)
                        meta = CacheFile(name, abspath, path, entry.stat(), isdir)
                        self.meta[meta.path] = meta
                    for v in self.meta.values():
                        try:
                            v.get_crc32()
                        except FileNotFoundError:
                            logger.debug('file not found, canceling')
                            del self.meta[v.path]
                        except PermissionError:
                            logger.debug('permission error, canceling')
                            del self.meta[v.path]
                    count += 1
                    SigProgress().set_progress((count / total) * 100)
            else:
                if any((
                            '\\.git' in rel_path,
                            '\\temp' in rel_path,
                )):
                    pass
                else:
                    logger.debug('re-building cache for path: {}'.format(rel_path))
                    path = rel_path
                    abspath = os.path.abspath(rel_path)
                    name = os.path.basename(rel_path)
                    isdir = os.path.isdir(abspath)
                    try:
                        meta = CacheFile(name, abspath, path, os.stat(abspath), isdir)
                        meta.get_crc32()
                    except FileNotFoundError:
                        logger.debug('file not found, canceling')
                    except PermissionError:
                        logger.debug('permission error, canceling')
                    else:
                        self.meta[meta.path] = meta
        finally:
            self.__is_building = False

    def stop(self):
        self.observer.stop()

    def temp_file(self, *, subdir: str, suffix: str = None, prefix: str = None) -> Path:
        subdir = Path(self.path.joinpath('temp').joinpath(subdir))
        subdir.makedirs_p()
        return create_temp_file(create_in_dir=str(subdir.abspath()), prefix=prefix, suffix=suffix)

    def temp_dir(self, *, subdir: str, suffix: str = None, prefix: str = None) -> Path:
        subdir = Path(self.path.joinpath('temp').joinpath(subdir))
        subdir.makedirs_p()
        return create_temp_dir(create_in_dir=str(subdir.abspath()), prefix=prefix, suffix=suffix)

    def wipe_temp(self):
        logger.debug('wiping temp dir')
        temp_dir = Path(self.path.joinpath('temp'))
        if not temp_dir.exists():
            return
        for path in temp_dir.listdir():
            if path.isdir():
                path.rmtree()
            elif path.isfile():
                path.remove()

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
    logger.info('initializing')
    from src.cfg import Config
    p = Path(Config().cache_path)
    logger.debug('cache will be in: {}'.format(p.abspath()))
    if not p.exists():
        logger.debug('directory does not exist, creating')
        p.makedirs()
    Cache(p).wipe_temp()
    logger.info('initialized')
