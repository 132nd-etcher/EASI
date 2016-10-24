# coding=utf-8

import os

from pytest_mock import MockFixture
from unittest import mock, skipUnless
from src.low.custom_path import Path

from src.helper.kdiff import KdiffHelper


class TestKdiff:
    def test_basics(self, config):
        kdiff = KdiffHelper()
        assert kdiff.path.abspath() == config.kdiff_path
        assert kdiff.is_installed is False
        assert kdiff.name == 'kdiff3'
        assert kdiff.folder == os.path.dirname(config.kdiff_path)

    @skipUnless(os.getenv('DOLONGTESTS', False) is not False, 'skipping long tests')
    def test_install(self, config, mocker: MockFixture, chtmpdir):
        progress_patch = mock.patch('src.helper.kdiff.SigProgress')
        progress = progress_patch.start()
        msg_patch = mock.patch('src.helper.kdiff.SigMsg.show')
        msg = msg_patch.start()
        with mock.patch(
                'src.helper.kdiff.KdiffHelper.path',
                new=mocker.PropertyMock(return_value=Path(str(chtmpdir.mkdir('kdiff').join('kdiff3.exe'))))):
            kdiff = KdiffHelper()
            # assert kdiff.path == Path(str(tmpdir.join('kdiff').join('kdiff3.exe'))).abspath()
            # return
            assert kdiff.path.abspath() == Path(str(chtmpdir.join('kdiff').join('kdiff3.exe'))).abspath()
            assert not os.path.exists(kdiff.path)
            assert kdiff.is_installed is False
            kdiff.download_and_install()
            assert os.path.exists(kdiff.path.abspath())
            assert kdiff.is_installed is True
            progress.assert_has_calls(mocker.call('set_progress(0))'), any_order=True)
            progress.assert_has_calls(mocker.call('set_progress(100))'), any_order=True)
            progress.assert_has_calls(mocker.call("set_progress_title('Unzipping KDiff3')"), any_order=True)
            assert msg.call_count == 1
            msg.assert_has_calls([mock.call('Success', 'KDiff3 has been successfully installed !')], any_order=True)
        progress_patch.stop()
        msg_patch.stop()

