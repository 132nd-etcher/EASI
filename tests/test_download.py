# coding=utf-8

import time
from hypothesis import strategies as st, given
from unittest import TestCase
from unittest.mock import MagicMock
from src.dld.download import downloader, DownloadError, FileDownload
from src.abstract.abstract_progress import ProgressInterface
from src.low.custom_path import Path

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


class TestDownload(TestCase):

    def setUp(self):
        self.wrong_url = [
            r'https://raw.githubusercontent.com/132nd-etcher/kdiff3/master/Qt5Coree.dll',
            'caribou'
        ]
        self.url1 = r'https://raw.githubusercontent.com/132nd-etcher/kdiff3/master/Qt5Core.dll'
        self.url2 = r'https://raw.githubusercontent.com/132nd-etcher/kdiff3/master/Qt5Gui.dll'
        self.progress = MagicMock()
        self.progress.set_text = MagicMock()
        self.progress.set_progress = MagicMock()

    def test_wrong_url(self):
        for x in self.wrong_url:
            fdl = downloader.download(x)
            self.assertFalse(fdl.success)
        for x in self.wrong_url:
            def parse_test_results(fdl):
                assert isinstance(fdl, FileDownload)
                self.assertFalse(fdl.success)
                self.assertIsNotNone(fdl.err)
            fdl = downloader.download(x, callback=parse_test_results)
            fdl.wait()

    def test_local_file(self):
        FileDownload(url=self.url1, local_file='./test')
        FileDownload(url=self.url1, local_file=Path('./test'))

    @given(x=st.one_of(st.booleans(), st.floats(), st.integers()))
    def test_local_file_wrong_type(self, x):
        with self.assertRaises(TypeError):
            FileDownload(url=self.url1, local_file=x)

    def test_raw_download(self):
        fdl = FileDownload(url=self.url1)
        fdl.download()
        fdl.wait()
        self.assertSequenceEqual(fdl.local_file.crc32(), '497A9296')
        self.assertTrue(fdl.success)
        self.assertTrue(fdl.done)

    def test_single_download(self):
        fdl = downloader.download(url=self.url1, progress=self.progress)
        fdl.wait()
        self.assertSequenceEqual(fdl.local_file.crc32(), '497A9296')
        self.assertTrue(fdl.success)
        self.assertTrue(fdl.done)
        self.progress.set_progress.assert_called_with(100)
        self.progress.set_text.assert_called_with('Downloading:\n{}'.format(self.url1))

    def test_bulk_download(self):
        callback = MagicMock()
        fdl_list = []
        for x in file_list:
            fdl_list.append(FileDownload(x))
        bdl = downloader.bulk_download(fdl_list, self.progress, callback=callback)
        bdl.wait()
        time.sleep(0.2)
        for fdl in bdl.fdl_list:
            self.assertTrue(fdl.local_file.exists())
            self.assertTrue(fdl.local_file.isfile())
            self.assertTrue(fdl.local_file.size > 0)
        self.assertTrue(bdl.done)
        self.assertEqual(callback.call_count, 1)
