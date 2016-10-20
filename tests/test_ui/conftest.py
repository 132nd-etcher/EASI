# coding=utf-8

import pytest
from src.cfg.cfg import config
from src.ui.dialog_config.dialog import ConfigDialog

from src.ui.main_ui.main_ui import MainUi


@pytest.fixture()
def config_dialog(tmpdir):
    sg = str(tmpdir.mkdir('sg'))
    cache = str(tmpdir.mkdir('cache'))
    kdiff = tmpdir.join('kdiff3.exe')
    kdiff.write('')
    kdiff = str(kdiff)
    config.saved_games_path = sg
    config.cache_path = cache
    config.kdiff_path = kdiff
    dialog = ConfigDialog()
    dialog.show()
    dialog.setup()
    yield dialog, sg, cache, kdiff
    dialog.close()


@pytest.fixture()
def mock_main_ui(mocker):
    yield mocker.patch('src.ui.base.with_signal.main_ui',
                       spec=MainUi,
                       some_obj=mocker.MagicMock(),
                       sig_proc=mocker.MagicMock(
                           do=mocker.MagicMock()),
                       msgbox=mocker.MagicMock(),
                       )


@pytest.fixture()
def main_ui(qtbot):
    _main_ui = MainUi(None)
    qtbot.add_widget(_main_ui)
    yield _main_ui
    _main_ui.exit()
