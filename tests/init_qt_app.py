# coding=utf-8
from unittest import TestCase

from src.low.singleton import Singleton
from src.main import main


class QtApp(metaclass=Singleton):
    def __init__(self):
        qt_app, main_ui = main(init_only=True, test_run=True)
        self.qt_app = qt_app
        self.main_ui = main_ui


class QtTestCase(TestCase):
    def __init__(self, *args, **kwargs):
        TestCase.__init__(self, *args, **kwargs)
        self.__qt_app = QtApp()
        self.qt_app = self.__qt_app.qt_app
        self.main_ui = self.__qt_app.main_ui
