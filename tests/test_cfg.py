# coding=utf-8

from src.cfg.cfg import Config
from .utils import ContainedTestCase


class TestConfig(ContainedTestCase):
    def __init__(self, *args, **kwargs):
        super(TestConfig, self).__init__(*args, **kwargs)
        self.config_path = None

    def setUp(self):
        super(TestConfig, self).setUp()
        self.config_path = self.create_temp_file()
        self.config = Config(config_file=self.config_path)

    # noinspection PyUnresolvedReferences
    def test_import(self):
        import src.cfg.values
        import src.cfg.cfg

        # def test_init(self):
        #     self.config.debug()
