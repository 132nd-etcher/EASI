# coding=utf-8

import string
import pytest
import subprocess

from hypothesis import strategies as st, given

from src.low.custom_path import Path
from .utils import ContainedTestCase


def test_get_version():
    import os
    p = Path(r'c:\windows\explorer.exe')
    assert p.isfile()
    assert p.exists()
    assert p.get_win32_file_info()
    info = p.get_win32_file_info()
    if os.environ.get('APPVEYOR'):
        assert p.get_win32_file_info().file_version == '6.3.9600.17031 (winblue_gdr.140221-1952)'
        assert info.file_version == '6.1.7600.16385 (win7_rtm.090713-1255)'
        assert info.fixed_version == '6.1.7601.23537'
        assert info.product_version == '6.3.9600.17031'
    else:
        assert info.file_version == '6.1.7600.16385 (win7_rtm.090713-1255)'
        assert info.fixed_version == '6.1.7601.23537'
        assert info.product_version == '6.1.7600.16385'
    assert info.comments is None
    assert info.company_name == 'Microsoft Corporation'
    assert info.copyright == '© Microsoft Corporation. All rights reserved.'
    assert info.file_description == 'Windows Explorer'
    assert info.internal_name == 'explorer'
    assert info.private_build is None
    assert info.original_filename == 'EXPLORER.EXE.MUI'
    assert info.product_name == 'Microsoft® Windows® Operating System'
    assert info.special_build is None
    assert info.trademark is None
    with pytest.raises(FileNotFoundError):
        Path('c:\explorer.exe').get_win32_file_info()
    with pytest.raises(TypeError):
        Path('c:\windows').get_win32_file_info()
    with pytest.raises(ValueError):
        p = Path('src/main.py.py')
        if not p.exists():
            p = Path('../src/main.py')
        p.get_win32_file_info()


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
