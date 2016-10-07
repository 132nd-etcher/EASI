# coding=utf-8

from hypothesis import strategies as st, given
from tests.init_qt_app import QtTestCase
from src.ui import ConfirmDialog
from PyQt5.QtCore import QTimer


class TestConfigDialog(QtTestCase):

    def test_confirm_dialog(self):
        question = 'some question'
        title = 'some title'
        dialog = ConfirmDialog(question, title)
        dialog.show()
        QTimer.singleShot(0, dialog.buttonBox.button(dialog.buttonBox.Yes).clicked)
        self.assertTrue(dialog.exec())
        dialog = ConfirmDialog(question, title)
        dialog.show()
        QTimer.singleShot(0, dialog.buttonBox.button(dialog.buttonBox.No).clicked)
        self.assertFalse(dialog.exec())