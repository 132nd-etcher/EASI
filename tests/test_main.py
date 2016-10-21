# coding=utf-8

import sys

from blinker_herald import signals
from pytestqt.qtbot import QtBot

test_succeeded = False


@signals.post_start_app.connect
def success(sender, signal_emitter, result):
    global test_succeeded
    test_succeeded = result


def test_and_exit(qtbot: QtBot):
    sys.argv.append('test_and_exit')
    from src import main
    main.main()
    sys.argv.pop()
    qtbot.wait_until(lambda: test_succeeded is True, timeout=15000)
