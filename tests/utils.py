# coding=utf-8

import os
import shutil
import stat
from unittest import TestCase

from src.low.custom_path import create_temp_dir, create_temp_file
from src.qt import QApplication
from src.low.singleton import Singleton
from src.main import main


class TempDir(object):
    @staticmethod
    def __force_rm_handle(remove_path, path, _):
        os.chmod(
            path,
            os.stat(path).st_mode | stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH
        )
        remove_path(path)

    def __enter__(self):
        self.temp_dir = create_temp_dir()
        return self.temp_dir

    def __exit__(self, exc_type, exc_value, traceback):
        if self.temp_dir.exists():

            def on_error(func, path, exc_info):
                self.__force_rm_handle(func, path, exc_info)

            shutil.rmtree(
                self.temp_dir.abspath(),
                onerror=on_error
            )
            if self.temp_dir.exists():
                raise Exception('failed to delete tempdir')


class ContainedTestCase(TestCase):
    def __init__(self, *args, **kwargs):
        super(ContainedTestCase, self).__init__(*args, **kwargs)

    def setUp(self):
        super(ContainedTestCase, self).setUp()
        self.temp_dir_context_manager = TempDir()
        self.temp_dir = self.temp_dir_context_manager.__enter__()

    def tearDown(self):
        self.temp_dir_context_manager.__exit__(None, None, None)
        super(ContainedTestCase, self).tearDown()

    def create_temp_dir(self, suffix='', prefix='', create_in_dir=None):
        if create_in_dir is None:
            create_in_dir = self.temp_dir.abspath()
        return create_temp_dir(suffix=suffix, prefix=prefix, create_in_dir=create_in_dir)

    def create_temp_file(self, suffix='', prefix='', create_in_dir=None):
        if create_in_dir is None:
            create_in_dir = self.temp_dir.abspath()
        return create_temp_file(suffix=suffix, prefix=prefix, create_in_dir=create_in_dir)


class SingletonQtApp(metaclass=Singleton):
    def __init__(self):
        qt_app, main_ui = main(init_only=True, test_run=True)
        self.qt_app = qt_app
        self.main_ui = main_ui


class QtTestCase(ContainedTestCase):
    def __init__(self, *args, **kwargs):
        TestCase.__init__(self, *args, **kwargs)
        singleton_qt_app = SingletonQtApp()
        assert isinstance(singleton_qt_app.qt_app, QApplication)
        self.qt_app = singleton_qt_app.qt_app
        self.main_ui = singleton_qt_app.main_ui
