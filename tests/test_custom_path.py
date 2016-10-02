# coding=utf-8

from hypothesis import strategies as st, given
import os
import subprocess
import string

from src.low.custom_path import Path, create_temp_file
from tests.with_file import TestCaseWithTestFile


class TestCustomPath(TestCaseWithTestFile):
    def hash_file(self, path):
        return subprocess.check_output(['crc32', path]).decode().split(' ')[0][2:]

    def test_crc32(self):
        for p in [Path(f) for f in os.listdir('.')]:
            if p.isfile():
                self.assertEqual(p.crc32(), self.hash_file(p.abspath()))
            else:
                with self.assertRaises(TypeError):
                    p.crc32()
        p = Path()

    def test_get_version(self):
        p = Path(r'c:\windows\explorer.exe')
        self.assertTrue(p.isfile())
        self.assertTrue(p.exists())
        self.assertTrue(p.get_version_info())
        self.assertSequenceEqual(p.get_version_info(), '6.1.7601.17514')
        with self.assertRaises(FileNotFoundError):
            Path('c:\explorer.exe').get_version_info()
        with self.assertRaises(TypeError):
            Path('c:\windows').get_version_info()
        with self.assertRaises(ValueError):
            Path('src/main.py').get_version_info()


    @given(s=st.one_of(st.text(alphabet=string.ascii_letters, min_size=1), st.none()),
           p=st.one_of(st.text(alphabet=string.ascii_letters, min_size=1), st.none()),
           d=st.one_of(st.text(alphabet=string.ascii_letters, min_size=1), st.none()))
    def test_create_temp_file(self, s, p, d):
        p = Path(create_temp_file(suffix=s, prefix=p))
        self.assertTrue(all([p.exists(), p.isfile()]))

