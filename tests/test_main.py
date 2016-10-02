# coding=utf-8

from tests.init_qt_app import QtTestCase
import time


class TestMain(QtTestCase):

    def test_import(self):
        # noinspection PyUnresolvedReferences
        from src import main

    def test_and_exit(self):
        import sys
        from src import main
        sys.argv.append('test_and_exit')
        main.main()
        sys.argv.pop()
        time.sleep(1)

    # def test_init_only(self):
    #     from src import main
    #     main.main(init_only=True, test_run=True)
    #     time.sleep(1)

    # def test_test_run(self):
    #     from src import main
    #     main.main(test_run=True)
    #     time.sleep(1)

