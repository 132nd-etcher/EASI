# coding=utf-8

import sys

import pytest
from blinker_herald import signals
from pytestqt.qtbot import QtBot

test_succeeded = False


@signals.post_start_app.connect
def success(sender, signal_emitter, result):
    assert sender == 'main'
    assert signal_emitter.__name__ == 'start_app'
    global test_succeeded
    test_succeeded = result


def test_and_exit(qtbot: QtBot):
    sys.argv.append('test_and_exit')
    sys.argv.append('no_qt_app')
    from src.easi import easi
    try:
        easi.start_gui()
        from src.ui.main_ui import MainUi
        MainUi.do(None, 'exit', 0)
    finally:
        import os
        del os.environ['REQUESTS_CA_BUNDLE']
    sys.argv.pop()
    sys.argv.pop()
    qtbot.wait_until(lambda: test_succeeded is True, timeout=15000)


def test_cert_verify(mocker, tmpdir):
    import os
    p = str(tmpdir.join('cacert.pem'))
    with open(p, 'w') as f:
        f.write('caribou')
    with pytest.raises(KeyError):
        assert os.environ['REQUESTS_CA_BUNDLE'] == ''
    from src.easi.easi import check_cert
    check_cert()
    assert os.environ['REQUESTS_CA_BUNDLE'] is not None
    assert os.path.exists(os.environ['REQUESTS_CA_BUNDLE'])
    mocker.patch('certifi.where', return_value=p)
    with pytest.raises(ImportError):
        check_cert()
