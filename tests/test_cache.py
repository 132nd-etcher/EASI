# coding=utf-8
import os
import time
from unittest import TestCase

from src.cache.cache import Cache
from src.low.custom_path import Path, create_temp_dir, create_temp_file
from src.low.singleton import Singleton


class TestCache(TestCase):
    def test_cache_init(self):
        Singleton.wipe_instances()
        with self.assertRaises(ValueError):
            Cache()
        td = create_temp_dir()
        Cache(td)
        Singleton.wipe_instances()
        td2 = os.path.join(td, 'cache')
        self.assertTrue(os.path.exists(td))
        self.assertFalse(os.path.exists(td2))
        Cache(td2)
        self.assertTrue(os.path.exists(td2))

    def test_meta_population(self):
        Singleton.wipe_instances()
        td = create_temp_dir()
        c = Cache(td)
        random_files = set()
        for _ in range(20):
            f = Path(create_temp_file(create_in_dir=c.path.abspath()))
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
        if os.getenv('APPVEYOR'):
            time.sleep(2)
        self.assertGreater(f1.mtime, mtime1)
        while c.is_building:
            pass
        self.assertSequenceEqual(c[f1.abspath()].crc32, f1.crc32())
        self.assertSequenceEqual(c[f1.abspath()].name, f1.name)
        self.assertSequenceEqual(c[f1.abspath()].path, f1.abspath())
