# coding=utf-8
import os
import time

from src.low.custom_path import Path

from src.cache.cache import Cache
from src.low.singleton import Singleton

from .utils import ContainedTestCase


class TestCache(ContainedTestCase):
    def __init__(self, test_method):
        super(TestCache, self).__init__(test_method)
        self.caches_obj = []

    def create_cache_obj(self, *args, **kwargs):
        self.caches_obj.append(Cache(*args, **kwargs))
        return self.caches_obj[-1]

    def tearDown(self):
        for cache_obj in self.caches_obj:
            assert isinstance(cache_obj, Cache)
            cache_obj.observer.stop()
        super(TestCache, self).tearDown()

    def test_cache_init(self):
        Singleton.wipe_instances()
        with self.assertRaises(ValueError):
            self.create_cache_obj()
        td = self.create_temp_dir()
        self.create_cache_obj(td)
        Singleton.wipe_instances()
        td2 = os.path.join(td, 'cache')
        self.assertTrue(os.path.exists(td))
        self.assertFalse(os.path.exists(td2))
        self.create_cache_obj(td2)
        self.assertTrue(os.path.exists(td2))

    def test_meta_population(self):
        Singleton.wipe_instances()
        td = self.create_temp_dir()
        c = self.create_cache_obj(td)
        random_files = set()
        for _ in range(20):
            f = Path(self.create_temp_file(create_in_dir=c.path.abspath()))
            random_files.add(f)
        while c.is_building:
            pass
        for f in random_files:
            self.assertTrue(f.abspath() in c)
        for f in c:
            self.assertSequenceEqual(f.crc32, '00000000')
        f1 = Path(random_files.pop())
        mtime1 = f1.mtime
        f1.write_bytes(os.urandom(1024))
        time.sleep(2)
        self.assertGreater(f1.mtime, mtime1)
        while c.is_building:
            pass
        self.assertSequenceEqual(c[f1.abspath()].crc32, f1.crc32())
        self.assertSequenceEqual(c[f1.abspath()].name, f1.name)
        self.assertSequenceEqual(c[f1.abspath()].path, f1.abspath())
