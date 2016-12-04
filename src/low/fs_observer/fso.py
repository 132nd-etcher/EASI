# coding=utf-8

import abc
import os

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from src.low.fs_observer.fso_event import FSOEvent
from src.low.fs_observer.fso_file import FSOFile
from src.low.custom_logging import make_logger
from src.low.custom_path import Path
from src.sig import SigProgress

from src.threadpool.threadpool import ThreadPool

logger = make_logger(__name__)


class FSObserver(FileSystemEventHandler):
    def __init__(self, path: str or Path):
        FileSystemEventHandler.__init__(self)
        if isinstance(path, str):
            path = Path(path)
        if not path.exists():
            raise FileNotFoundError(path.abspath())
        self._fso_path = path

        self._fso_pool = ThreadPool(_num_threads=1, _basename='FSO', _daemon=True)

        self._fso_observer = Observer()
        self._fso_observer.schedule(self, self._fso_path, recursive=True)
        self._fso_observer.start()
        self._fso_meta = {}
        self._fso_is_building = False
        self._fso_build()

    @abc.abstractmethod
    def fso_on_event(self, event: FSOEvent):
        """"""

    @property
    def is_building(self):
        return self._fso_is_building

    @staticmethod
    def __filter_event(event):
        if '\\.git\\' in event.src_path:
            return False
        return True

    def on_created(self, event):
        if self.__filter_event(event):
            logger.debug('{}'.format(event.src_path))
            self._fso_build(rel_path=event.src_path)
            self.fso_on_event(FSOEvent('created', event.src_path))

    def on_modified(self, event):
        if self.__filter_event(event):
            logger.debug('{}'.format(event.src_path))
            self._fso_build(rel_path=event.src_path)
            self.fso_on_event(FSOEvent('modified', event.src_path))

    def on_moved(self, event):
        if self.__filter_event(event):
            logger.debug('{} -> {}'.format(event.src_path, event.dest_path))
            try:
                del self._fso_meta[event.src_path]
            except KeyError:
                # Src wasn't in the cache anyway
                pass
            self._fso_build(rel_path=event.dest_path)
            self.fso_on_event(FSOEvent('moved', event.src_path, event.dest_path))

    def on_deleted(self, event):
        if self.__filter_event(event):
            logger.debug('{}'.format(event.src_path))
            for path in list(self._fso_meta.keys()):
                if path.startswith('{}\\'.format(event.src_path)):
                    del self._fso_meta[path]
            try:
                del self._fso_meta[event.src_path]
            except KeyError:
                logger.debug('not in cache, skipping')
                pass
            self.fso_on_event(FSOEvent('deleted', event.src_path))

    def _fso_build(self, rel_path : str = None):
        self._fso_pool.queue_task(
            self._fso_build_,
            kwargs=dict(rel_path=rel_path)
        )

    def _fso_build_(self, rel_path: str = None):
        self._fso_is_building = True
        try:
            if rel_path is None:
                logger.info('re-building whole cache folder')
                SigProgress().set_progress(0)
                SigProgress().set_progress_text('Building local cache')
                self._fso_meta = {}
                total = 0
                count = 0
                for root, folders, _ in os.walk(self._fso_path, topdown=True):
                    folders[:] = [d for d in folders if d not in ['.git']]
                    folders[:] = [d for d in folders if d not in ['temp']]
                    # noinspection PyUnusedLocal
                    for x in os.scandir(root):
                        abspath = os.path.join(self._fso_path.dirname(), x.path)
                        if '\\.git\\' in abspath or abspath.endswith('\\.git'):
                            continue
                        if '\\temp\\' in abspath or abspath.endswith('\\temp'):
                            continue
                        total += 1
                for root, folders, _ in os.walk(self._fso_path, topdown=True):
                    folders[:] = [d for d in folders if d not in ['.git']]
                    folders[:] = [d for d in folders if d not in ['temp']]
                    for entry in os.scandir(root):
                        path = entry.path
                        abspath = os.path.join(self._fso_path.dirname(), path)
                        if '\\.git\\' in abspath or abspath.endswith('\\.git'):
                            continue
                        if '\\temp\\' in abspath or abspath.endswith('\\temp'):
                            continue
                        path = entry.path
                        abspath = os.path.join(self._fso_path.dirname(), path)
                        name = entry.name
                        isdir = os.path.isdir(abspath)
                        meta = FSOFile(name, abspath, path, entry.stat(), isdir)
                        self._fso_meta[meta.path] = meta
                for v in self._fso_meta.values():
                    try:
                        v.get_crc32()
                    except FileNotFoundError:
                        logger.debug('file not found, canceling')
                        del self._fso_meta[v.path]
                    except PermissionError:
                        logger.debug('permission error, canceling')
                        del self._fso_meta[v.path]
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
                        meta = FSOFile(name, abspath, path, os.stat(abspath), isdir)
                        meta.get_crc32()
                    except FileNotFoundError:
                        logger.debug('file not found, canceling')
                    except PermissionError:
                        logger.debug('permission error, canceling')
                    else:
                        self._fso_meta[meta.path] = meta
        finally:
            self._fso_is_building = False

    def stop(self):
        self._fso_observer.stop()

    def all_done(self):
        return self._fso_pool.all_done()

    def __len__(self):
        return len(self._fso_meta)

    def __getitem__(self, item) -> FSOFile:
        try:
            return self._fso_meta.__getitem__(item)
        except KeyError:
            return self._fso_meta.__getitem__(Path(item).relpath(self._fso_path))

    def __contains__(self, item) -> bool:
        try:
            self.__getitem__(item)
            return True
        except KeyError:
            return False

    def __str__(self):
        out = ['cache object']
        for k in self._fso_meta.keys():
            out.append('{}: {}'.format(k, self._fso_meta[k]))
        return '\n\t'.join(out)

    def __iter__(self):
        for item in self._fso_meta.values():
            yield item