# coding=utf-8

import pytest


# noinspection PyUnusedLocal
@pytest.fixture()
def config_dialog(qtbot, tmpdir, config):
    """Returns initialized src.ui.dialog_config.ConfigDialog"""
    from src.ui.dialog_config.dialog import ConfigDialog
    print('creating dummy config')
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
    yield dialog, sg, cache, kdiff, config
    dialog.close()


@pytest.fixture()
def mock_main_ui(mocker):
    """Returns a dummy MainUi object that can handle connected objects"""
    from src.ui.main_ui import MainUi
    yield mocker.patch('src.low.constants.MAIN_UI',
                       spec=MainUi,
                       some_obj=mocker.MagicMock(),
                       do=mocker.MagicMock(),
                       sig_proc=mocker.MagicMock(
                           do=mocker.MagicMock()),
                       msgbox=mocker.MagicMock(),
                       )


@pytest.fixture()
def main_ui(qtbot):
    """Returns the *real* MainUi object running in a QEventLoop"""
    from src.ui.main_ui import MainUi
    _main_ui = MainUi()
    qtbot.add_widget(_main_ui)
    yield _main_ui
    _main_ui.exit()
