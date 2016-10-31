# coding=utf-8
import time
import abc

from ruamel.yaml import dump as ydump, load as yload, RoundTripDumper

from src.meta.abstract import AbstractMeta
from src.low.custom_logging import make_logger
from src.low.custom_path import Path

logger = make_logger(__name__)


class Meta(AbstractMeta):

    @property
    @abc.abstractproperty
    def meta_header(self):
        """"""

    def __init__(self, path: str or Path, init_dict: dict = None, auto_read=True, encrypted=False):
        self.free = True
        self.encrypt = encrypted
        if init_dict is None:
            self._data = {}
        else:
            if not isinstance(init_dict, dict):
                raise TypeError('expected a dict, got "{}"'.format(type(init_dict)))
            self._data = init_dict
        self._values, self._keys, self._items = None, None, None
        self._init_views()
        if isinstance(path, Path):
            pass
        elif isinstance(path, str):
            path = Path(path)
        else:
            raise TypeError('expected a Path or a str, got: {}'.format(type(path)))
        self._path = path
        if auto_read:
            self.read()

    @property
    def path(self) -> Path:
        return self._path

    @path.setter
    def path(self, value: str or Path):
        if isinstance(value, Path):
            pass
        elif isinstance(value, str):
            value = Path(value)
        else:
            raise TypeError('expected Path or str, got: {}'.format(type(value)))
        self._path = value

    def _init_views(self):
        self._values = self._data.values()
        self._keys = self._data.keys()
        self._items = self._data.items()

    @property
    def data(self):
        return self._data

    def get_context(self):
        """Used to populate Sentry context"""
        return self.data

    @data.setter
    def data(self, value: dict):
        if not isinstance(value, dict):
            raise TypeError('expected a dict, got "{}"'.format(type(value)))
        self._data = value
        self._init_views()

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        for k in self.keys():
            yield k

    def __contains__(self, x):
        return self._data.__contains__(x)

    def __delitem__(self, key):
        del self.data[key]

    def __setitem__(self, key, value, _write=False):
        self.data[key] = value
        if _write:
            self.write()

    def __getitem__(self, key):
        # return self._data.__getitem__(key)
        return self._data.get(key, None)

    def __str__(self):
        return self.data.__str__()

    def __repr__(self):
        return '{}: {}'.format(self.__class__.__name__, self.data.__repr__())

    def get(self, key, default=None):
        return self._data.get(key, default)

    def keys(self):
        """
        Shadows default dict().keys() method
        :return: keys
        """
        return self._keys

    def values(self):
        return self._values

    def items(self):
        return self._items

    def debug(self, txt: str):
        logger.debug('{}: {}'.format(self.path.abspath(), txt))

    def exception(self, txt: str):
        logger.debug('{}: {}'.format(self.path.abspath(), txt))

    def dump(self):
        return ydump(self.data, Dumper=RoundTripDumper, default_flow_style=False)
        # return jdumps(self.data, indent=True, sort_keys=True)

    def load(self, data):
        self.data = yload(data)
        # return jloads(data)

    def read(self):
        """
        Reads the local Config file
        """
        # self.debug('reading file')
        self.wait_for_lock()
        try:
            if self.path.exists():
                if self.path.getsize() == 0:
                    self.debug('{}: removing existing empty file: {}'.format(self.__class__.__name__, self.path))
                    self.path.remove()
                    return
                try:
                    if self.encrypt:
                        self.load(self.path.bytes())
                    else:
                        self.load(self.path.text(encoding='utf8'))
                    # self.debug('file read successful')
                except ValueError:
                    raise ValueError('{}: metadata file corrupted'.format(self.path.abspath()))
                else:
                    try:
                        if not self.data['header'] == self.meta_header:
                            raise TypeError('meta-header mismatch, expected: "{}", got: "{}" on file: {}'.format(
                                self.meta_header, self.data['header'], self.path.abspath()
                            ))
                        else:
                            del self.data['header']
                    except KeyError:
                        pass
        except OSError:
            self.exception('error while reading metadata file')
        finally:
            self.free = True

    @staticmethod
    def read_header(path):
        path = Path(path)
        data = yload(path.text(encoding='utf8'))
        return data['header']

    def write(self):
        """
        Writes the current config to the local Config file
        """
        if len(self._data) == 0:
            raise ValueError('no data to write')
        # self.debug('writing file')
        self.wait_for_lock()
        self.data['header'] = self.meta_header
        try:
            if self.encrypt:
                self.path.write_bytes(self.dump())
            else:
                self.path.write_text(self.dump(), encoding='utf8')
        except OSError:
            self.exception('error while writing metadata to file')
        finally:
            self.free = True

    def wait_for_lock(self):
        i = 0
        while not self.free:
            time.sleep(0.1)
            i += 1
            if i == 10:
                self.debug('waiting for resource lock')
                i = 0
        self.free = False
