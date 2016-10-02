# coding=utf-8

import abc
from unittest import TestCase

class Singleton(abc.ABCMeta):
    """
    When used as metaclass, allow only one instance of a class
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class QtApp(metaclass=Singleton):

    def __init__(self):
        from src.main import main
        qt_app, main_ui = main(init_only=True, test_run=True)
        self.qt_app = qt_app
        self.main_ui = main_ui


class QtTestCase(TestCase):

    def __init__(self, *args, **kwargs):
        TestCase.__init__(self, *args, **kwargs)
        self.__qt_app = QtApp()
        self.qt_app = self.__qt_app.qt_app
        self.main_ui = self.__qt_app.main_ui
