# coding=utf-8

import os
import time
from unittest.mock import MagicMock
from unittest import skipUnless

import pytest
from hypothesis import strategies as st, given

from src.dld.download import downloader, FileDownload

file_list = [
    r'http://www.textfiles.com/100/914bbs.txt',
    r'http://www.textfiles.com/100/ad.txt',
    r'http://www.textfiles.com/100/adventur.txt',
    r'http://www.textfiles.com/100/arttext.fun',
    r'http://www.textfiles.com/100/bc760mod.ham',
    r'http://www.textfiles.com/100/black.box',
    r'http://www.textfiles.com/100/cDc-0200.txt',
    r'http://www.textfiles.com/100/crossbow',
    r'http://www.textfiles.com/100/gems.txt',
    r'http://www.textfiles.com/100/krckwczt.app',
]


class TestDownload:
    # noinspection SpellCheckingInspection
    wrong_url = [
        r'https://raw.githubusercontent.com/132nd-etcher/kdiff3/master/Qt5Coree.dll',
        'caribou'
    ]
    url1 = r'https://raw.githubusercontent.com/132nd-etcher/kdiff3/master/Qt5Core.dll'
    url2 = r'https://raw.githubusercontent.com/132nd-etcher/kdiff3/master/Qt5Gui.dll'

    progress = None

    @pytest.fixture(autouse=True)
    def make_progress(self):
        self.progress = MagicMock()
        self.progress.set_progress_text = MagicMock()
        self.progress.set_progress = MagicMock()

    @given(x=st.one_of(st.booleans(), st.floats(), st.integers()))
    def test_local_file_wrong_type(self, x):
        with pytest.raises(TypeError):
            FileDownload(url=self.url1, local_file=x)

    def test_wrong_url(self, tmpdir):
        for x in self.wrong_url:
            fdl = downloader.download(url=x, local_file=str(tmpdir.join('f')))
            fdl.wait()
            assert not fdl.success
            assert fdl.done
        for x in self.wrong_url:
            def parse_test_results(_fdl):
                assert isinstance(_fdl, FileDownload)
                assert not _fdl.success
                assert _fdl.err is not None

            fdl = downloader.download(x, local_file=str(tmpdir.join('ff')), callback=parse_test_results)
            fdl.wait()

    def test_local_file(self, tmpdir):
        FileDownload(url=self.url1, local_file=str(tmpdir.join('f')))

    def test_raw_download(self, tmpdir):
        fdl = FileDownload(url=self.url1, local_file=str(tmpdir.join('f')))
        fdl.download()
        fdl.wait()
        assert fdl.local_file.crc32() == '497A9296'
        assert fdl.success
        assert fdl.done

    def test_single_download(self, tmpdir):
        fdl = downloader.download(url=self.url1, local_file=str(tmpdir.join('f')), progress=self.progress)
        fdl.wait()
        assert fdl.local_file.crc32() == '497A9296'
        assert fdl.success
        assert fdl.done
        self.progress.set_progress.assert_called_with(100)
        self.progress.set_progress_text.assert_called_with('Downloading:\n{}'.format(self.url1))

    @skipUnless(os.getenv('DOLONGTESTS', False) is not False, 'skipping long tests')
    def test_bulk_download(self, tmpdir):
        callback = MagicMock()
        fdl_list = []
        for x in file_list:
            fdl_list.append(FileDownload(x, local_folder=str(tmpdir)))
        bdl = downloader.bulk_download(
            fdl_list=fdl_list,
            progress=self.progress,
            callback=callback)
        bdl.wait()
        time.sleep(0.2)
        for fdl in bdl.fdl_list:
            assert fdl.local_file.exists()
            assert fdl.local_file.isfile()
            assert fdl.local_file.size > 0
        assert bdl.done
        assert callback.call_count == 1
