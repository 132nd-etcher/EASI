# coding=utf-8

import pytest

from src.ui.main_ui.main_ui import MainUi


@pytest.fixture()
def main_ui(mocker):
    yield mocker.patch('src.abstract.ui.connected_object.main_ui',
                       spec=MainUi,
                       some_obj=mocker.MagicMock(),
                       sig_proc=mocker.MagicMock(
                           do=mocker.MagicMock()),
                       msgbox=mocker.MagicMock(),
                       #     show=mocker.MagicMock()),
                       )
