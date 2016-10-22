# coding=utf-8

import sys

import pytest
from blinker_herald import signals
from pytestqt.qtbot import QtBot

test_succeeded = False


@signals.post_start_app.connect
def success(sender, signal_emitter, result):
    global test_succeeded
    test_succeeded = result


def test_and_exit(qtbot: QtBot):
    sys.argv.append('test_and_exit')
    sys.argv.append('no_qt_app')
    from src import easi
    easi.start_gui()
    sys.argv.pop()
    sys.argv.pop()
    qtbot.wait_until(lambda: test_succeeded is True, timeout=15000)
    import os
    del os.environ['REQUESTS_CA_BUNDLE']


def test_cert_verify(mocker, tmpdir):
    import os
    p = str(tmpdir.join('cacert.pem'))
    with open(p, 'w') as f:
        f.write('caribou')
    with pytest.raises(KeyError):
        assert os.environ['REQUESTS_CA_BUNDLE'] == ''
    from src.easi import check_cert
    check_cert()
    assert os.environ['REQUESTS_CA_BUNDLE'] is not None
    assert os.path.exists(os.environ['REQUESTS_CA_BUNDLE'])
    mocker.patch('certifi.where', return_value=p)
    with pytest.raises(ImportError):
        check_cert()
