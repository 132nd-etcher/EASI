# coding=utf-8

from PyQt5.QtCore import QTimer

from src.ui import ConfirmDialog
from tests.init_qt_app import QtTestCase


class TestConfigDialog(QtTestCase):
    def test_confirm_dialog(self):
        question = 'some question'
        title = 'some title'
        dialog = ConfirmDialog(question, title)
        dialog.show()
        # noinspection PyCallByClass,PyTypeChecker
        QTimer.singleShot(0, dialog.buttonBox.button(dialog.buttonBox.Yes).clicked)
        self.assertTrue(dialog.exec())
        dialog = ConfirmDialog(question, title)
        dialog.show()
        # noinspection PyCallByClass,PyTypeChecker
        QTimer.singleShot(0, dialog.buttonBox.button(dialog.buttonBox.No).clicked)
        self.assertFalse(dialog.exec())
