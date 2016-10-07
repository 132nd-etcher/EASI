# coding=utf-8

from src.qt import QObject, QIcon, QLabel
from tests.init_qt_app import QtTestCase
from src.abstract.ui.base_dialog import AbstractBaseDialog
from src.abstract.ui.base_qobject import AbstractBaseQWidget


class TestAbstractBase(QtTestCase):

    def test_wrong_init(self):
        for x in [QObject, QLabel, QIcon, 'test', True, None, 32]:
            with self.assertRaises(TypeError):
                AbstractBaseDialog(x)
            with self.assertRaises(TypeError):
                AbstractBaseQWidget(x)




