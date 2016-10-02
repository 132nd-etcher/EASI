# coding=utf-8

from tests.init_qt_app import QtTestCase


class TestMain(QtTestCase):
    def test_import(self):
        # noinspection PyUnresolvedReferences
        from src import abstract
