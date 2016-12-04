# coding=utf-8

import pytest

from src.low.fs_observer.fso import FSOEvent, FSOFile, FSObserver
from src.low.custom_path import Path


def test_observer(tmpdir, mocker):
    tmpdir = Path(str(tmpdir))
    mock = mocker.MagicMock()
    obs = FSObserver(tmpdir.abspath())
    obs.fso_on_event = mock
    assert mock.call_count == 0
    tmpdir.joinpath('file').write_text('')
    while not obs.all_done():
        pass
    assert mock.call_count == 1
    tmpdir.joinpath('folder').mkdir()
    assert mock.call_count == 2


