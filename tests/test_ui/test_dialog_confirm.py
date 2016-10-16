# coding=utf-8

from pytestqt.qtbot import QtBot

from src.qt import Qt
from src.ui import ConfirmDialog

question = 'some question'
title = 'some title'


def test_init(qtbot: QtBot):
    dialog = ConfirmDialog(question, title)
    qtbot.add_widget(dialog)
    dialog.show()
    qtbot.wait_for_window_shown(dialog)
    assert dialog.windowTitle() == title
    assert dialog.label.text() == question


def test_confirm_dialog_ok(qtbot: QtBot):
    dialog = ConfirmDialog(question, title)
    qtbot.add_widget(dialog)
    dialog.show()
    qtbot.wait_for_window_shown(dialog)
    qtbot.mouseClick(dialog.btn_yes, Qt.LeftButton)
    assert dialog.result() == dialog.Accepted


def test_confirm_dialog_cancel(qtbot: QtBot):
    dialog = ConfirmDialog(question, title)
    qtbot.add_widget(dialog)
    dialog.show()
    qtbot.wait_for_window_shown(dialog)
    qtbot.mouseClick(dialog.btn_no, Qt.LeftButton)
    assert dialog.result() == dialog.Rejected
