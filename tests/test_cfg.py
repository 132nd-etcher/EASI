# coding=utf-8

from unittest import TestCase
import os


class TestConfig(TestCase):
    def __init__(self, *args, **kwargs):
        TestCase.__init__(self, *args, **kwargs)
        if os.path.exists('./test'):
            os.remove('./test')

    def setUp(self):
        from src.cfg.cfg import Config
        self.config = Config(config_file='./test')

    def tearDown(self):
        del self.config
        if os.path.exists('./test'):
            os.remove('./test')

    # noinspection PyUnresolvedReferences
    def test_import(self):
        import src.cfg.values
        import src.cfg.cfg

        # def test_init(self):
        #     self.config.debug()
