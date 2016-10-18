# coding=utf-8

import string
import subprocess

from hypothesis import strategies as st, given

from src.low.custom_path import Path
from .utils import ContainedTestCase


class TestCustomPath(ContainedTestCase):
    @staticmethod
    def hash_file(path):
        return subprocess.check_output(['crc32', path]).decode().split(' ')[0][2:]

    def test_crc32(self):
        import os
        for p in [Path(f) for f in os.listdir('.')]:
            if p.isfile():
                self.assertEqual(p.crc32(), self.hash_file(p.abspath()))
            else:
                with self.assertRaises(TypeError):
                    p.crc32()

    def test_get_version(self):
        import os
        p = Path(r'c:\windows\explorer.exe')
        self.assertTrue(p.isfile())
        self.assertTrue(p.exists())
        self.assertTrue(p.get_win32_file_info())
        if os.environ.get('APPVEYOR'):
            self.assertSequenceEqual(p.get_win32_file_info().file_version, '6.3.9600.17031 (winblue_gdr.140221-1952)')
        else:
            self.assertSequenceEqual(p.get_win32_file_info().file_version, '6.1.7600.16385 (win7_rtm.090713-1255)')
        with self.assertRaises(FileNotFoundError):
            Path('c:\explorer.exe').get_win32_file_info()
        with self.assertRaises(TypeError):
            Path('c:\windows').get_win32_file_info()
        with self.assertRaises(ValueError):
            Path('src/main.py').get_win32_file_info()

    def test_human_size(self):

        p = Path(self.create_temp_file())

        def __make_file(_len):
            with open(p.abspath(), 'wb') as f:
                if _len == 0:
                    return
                f.seek(_len - 1)
                f.write(b'0')

        __make_file(0)
        self.assertSequenceEqual(p.human_size(), '0B')
        __make_file(1)
        self.assertSequenceEqual(p.human_size(), '1B')
        __make_file(512)
        self.assertSequenceEqual(p.human_size(), '512B')
        __make_file(1024)
        self.assertSequenceEqual(p.human_size(), '1.0K')
        __make_file(1024 * 128)
        self.assertSequenceEqual(p.human_size(), '128.0K')
        __make_file(1024 * 1024)
        self.assertSequenceEqual(p.human_size(), '1.0M')
        __make_file((1024 * 1024 * 32) + (1024 * 128))
        self.assertSequenceEqual(p.human_size(), '32.1M')

    @given(s=st.one_of(st.text(alphabet=string.ascii_letters, min_size=1), st.none()),
           p=st.one_of(st.text(alphabet=string.ascii_letters, min_size=1), st.none()), )
    def test_create_temp_file(self, s, p):
        p = Path(self.create_temp_file(suffix=s, prefix=p))
        self.assertTrue(all([p.exists(), p.isfile()]))
