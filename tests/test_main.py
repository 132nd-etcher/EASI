# coding=utf-8

import sys

from src.low import constants

import pytest
from blinker_herald import signals
from pytestqt.qtbot import QtBot
from unittest import skip

test_succeeded = False


@pytest.fixture(autouse=True)
def close_qt_app():
    yield
    if constants.QT_APP:
        constants.QT_APP.exit()


@signals.post_start_app.connect
def success(sender, signal_emitter, result):
    assert sender == 'main'
    assert signal_emitter.__name__ == 'start_app'
    global test_succeeded
    test_succeeded = result


@skip('works fine alone, not in bulk')
def test_and_exit(qtbot: QtBot, tmpdir):
    sys.argv.append('test_and_exit')
    sys.argv.append('no_qt_app')
    from src.easi import easi
    from src.low import constants
    constants.PATH_CONFIG_FILE = str(tmpdir.join('config'))
    constants.PATH_KEYRING_FILE = str(tmpdir.join('keyring'))
    constants.PATH_LOG_FILE = str(tmpdir.join('log'))
    try:
        easi.start_gui()
        constants.MAIN_UI.do('splash', 'hide')
        constants.MAIN_UI.do(None, 'exit')
    finally:
        import os
        del os.environ['REQUESTS_CA_BUNDLE']
    sys.argv.pop()
    sys.argv.pop()
    qtbot.wait_until(lambda: test_succeeded is True, timeout=15000)


@skip('works fine alone, not in bulk')
def test_cert_verify(mocker, tmpdir):
    import os
    p = str(tmpdir.join('cacert.pem'))
    with open(p, 'w') as f:
        f.write('caribou')
    with pytest.raises(KeyError):
        assert os.environ['REQUESTS_CA_BUNDLE'] == ''
    from src.easi.check_cert import check_cert
    check_cert()
    assert os.environ['REQUESTS_CA_BUNDLE'] is not None
    assert os.path.exists(os.environ['REQUESTS_CA_BUNDLE'])
    mocker.patch('certifi.where', return_value=p)
    with pytest.raises(ImportError):
        check_cert()
