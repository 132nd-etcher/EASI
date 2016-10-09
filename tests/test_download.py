# coding=utf-8

import time
from unittest.mock import MagicMock

from hypothesis import strategies as st, given

from src.dld.download import downloader, FileDownload
from .utils import ContainedTestCase

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


class TestDownload(ContainedTestCase):
    def __init__(self, *args, **kwargs):
        super(TestDownload, self).__init__(*args, **kwargs)
        self.wrong_url = [
            r'https://raw.githubusercontent.com/132nd-etcher/kdiff3/master/Qt5Coree.dll',
            'caribou'
        ]
        self.url1 = r'https://raw.githubusercontent.com/132nd-etcher/kdiff3/master/Qt5Core.dll'
        self.url2 = r'https://raw.githubusercontent.com/132nd-etcher/kdiff3/master/Qt5Gui.dll'

    def setUp(self):
        super(TestDownload, self).setUp()
        self.progress = MagicMock()
        self.progress.set_progress_text = MagicMock()
        self.progress.set_progress = MagicMock()

    def test_wrong_url(self):
        for x in self.wrong_url:
            fdl = downloader.download(url=x, local_file=self.create_temp_file())
            self.assertFalse(fdl.success)
        for x in self.wrong_url:
            def parse_test_results(_fdl):
                assert isinstance(_fdl, FileDownload)
                self.assertFalse(_fdl.success)
                self.assertIsNotNone(_fdl.err)

            fdl = downloader.download(x, local_file=self.create_temp_file(), callback=parse_test_results)
            fdl.wait()

    def test_local_file(self):
        FileDownload(url=self.url1, local_file=self.create_temp_file())
        FileDownload(url=self.url1, local_file=self.create_temp_file())

    @given(x=st.one_of(st.booleans(), st.floats(), st.integers()))
    def test_local_file_wrong_type(self, x):
        with self.assertRaises(TypeError):
            FileDownload(url=self.url1, local_file=x)

    def test_raw_download(self):
        fdl = FileDownload(url=self.url1, local_file=self.create_temp_file())
        fdl.download()
        fdl.wait()
        self.assertSequenceEqual(fdl.local_file.crc32(), '497A9296')
        self.assertTrue(fdl.success)
        self.assertTrue(fdl.done)

    def test_single_download(self):
        fdl = downloader.download(url=self.url1, local_file=self.create_temp_file(), progress=self.progress)
        fdl.wait()
        self.assertSequenceEqual(fdl.local_file.crc32(), '497A9296')
        self.assertTrue(fdl.success)
        self.assertTrue(fdl.done)
        self.progress.set_progress.assert_called_with(100)
        self.progress.set_progress_text.assert_called_with('Downloading:\n{}'.format(self.url1))

    def test_bulk_download(self):
        callback = MagicMock()
        fdl_list = []
        for x in file_list:
            fdl_list.append(FileDownload(x, local_folder=self.create_temp_dir()))
        bdl = downloader.bulk_download(
            fdl_list=fdl_list,
            progress=self.progress,
            callback=callback)
        bdl.wait()
        time.sleep(0.2)
        for fdl in bdl.fdl_list:
            self.assertTrue(fdl.local_file.exists())
            self.assertTrue(fdl.local_file.isfile())
            self.assertTrue(fdl.local_file.size > 0)
        self.assertTrue(bdl.done)
        self.assertEqual(callback.call_count, 1)
