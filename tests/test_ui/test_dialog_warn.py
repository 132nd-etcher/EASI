# coding=utf-8

import pytest
from src.ui.dialog_warn.dialog_warn import WarningDialog
from src.qt import Qt


class TestWarnDialog:

    # noinspection PyUnusedLocal
    def test_basics(self, qtbot, config):
        dialog = WarningDialog('dummy_id', 'some text', 'title')
        qtbot.add_widget(dialog.qobj)
        assert dialog.qobj.label.text() == 'some text'
        assert dialog.qobj.windowTitle() == 'title'
        dialog.qobj.show()
        assert dialog.qobj.isVisible() is True
        qtbot.mouseClick(dialog.qobj.buttonBox.button(dialog.qobj.buttonBox.Ok), Qt.LeftButton)
        assert dialog.qobj.isVisible() is False

    # noinspection PyUnusedLocal
    def test_buttons(self, qtbot):
        WarningDialog('dummy_id', 'some text', 'title', 'ok')
        WarningDialog('dummy_id', 'some text', 'title', 'yesno')
        with pytest.raises(ValueError):
            WarningDialog('dummy_id', 'some text', 'title', 'something_else')

    def test_ack(self, qtbot, config):
        assert len(config.ack) == 0
        dialog = WarningDialog('dummy_id', 'some text', 'title')
        qtbot.add_widget(dialog.qobj)
        dialog.qobj.show()
        assert dialog.qobj.isVisible() is True
        qtbot.mouseClick(dialog.qobj.checkBox, Qt.LeftButton)
        qtbot.mouseClick(dialog.qobj.buttonBox.button(dialog.qobj.buttonBox.Ok), Qt.LeftButton)
        assert dialog.qobj.isVisible() is False
        assert len(config.ack) == 1
        dialog = WarningDialog('some text', 'title')
        qtbot.add_widget(dialog.qobj)
        assert dialog.qobj.isVisible() is False
        assert len(config.ack) == 1
        assert 'dummy_id' in config.ack
