# coding=utf-8

import pytest
from src.ui.dialog_warn.dialog_warn import WarningDialog
from src.qt import Qt


class TestWarnDialog:

    def test_basics(self, qtbot, config):
        dialog = WarningDialog('some text', 'title')
        qtbot.add_widget(dialog.qobj)
        assert dialog.qobj.label.text() == 'some text'
        assert dialog.qobj.windowTitle() == 'title'
        dialog.qobj.show()
        assert dialog.qobj.isVisible() is True
        qtbot.mouseClick(dialog.qobj.buttonBox.button(dialog.qobj.buttonBox.Ok), Qt.LeftButton)
        assert dialog.qobj.isVisible() is False

    def test_buttons(self, qtbot):
        WarningDialog('some text', 'title', 'ok')
        WarningDialog('some text', 'title', 'yesno')
        with pytest.raises(ValueError):
            WarningDialog('some text', 'title', 'somethingelse')

    def test_ack(self, qtbot, config):
        assert len(config.ack) == 0
        dialog = WarningDialog('some text', 'title')
        qtbot.add_widget(dialog.qobj)
        assert dialog.qobj.isVisible() is True
        qtbot.mouseClick(dialog.qobj.checkBox, Qt.LeftButton)
        qtbot.mouseClick(dialog.qobj.buttonBox.button(dialog.qobj.buttonBox.Ok), Qt.LeftButton)
        assert dialog.qobj.isVisible() is False
        assert len(config.ack) == 1
        dialog = WarningDialog('some text', 'title')
        qtbot.add_widget(dialog.qobj)
        assert dialog.qobj.isVisible() is False
        assert len(config.ack) == 1
