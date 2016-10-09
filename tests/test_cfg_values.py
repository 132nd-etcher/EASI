# coding=utf-8

import sys
import tempfile
from unittest import mock

from hypothesis import strategies as st, given

from src.cfg.values import ConfigValues
from src.meta import Meta
from .utils import ContainedTestCase


class C(Meta, ConfigValues):
    pass


class TestConfigValues(ContainedTestCase):

    def __init__(self, *args, **kwargs):
        super(TestConfigValues, self).__init__(*args, **kwargs)
        self.test_file = None

    def setUp(self):
        super(TestConfigValues, self).setUp()
        self.test_file = self.create_temp_file()
        self.c = C(self.test_file)

    @given(x=st.one_of(st.booleans(), st.floats(), st.none(), st.integers()))
    def test_type_error(self, x):
        with self.assertRaises(TypeError):
            self.c.saved_games_path = x

    def test_config_values(self):

        c = C(self.test_file)
        c.active_dcs_installation = 'test'
        c.write()
        with self.assertRaises(TypeError):
            c.saved_games_path = self.test_file
        with self.assertRaises(FileNotFoundError):
            c.saved_games_path = ''
        with mock.patch('src.sig.base_custom_signal.CustomSignal.send') as m:
            c.saved_games_path = tempfile.gettempdir()
            m.assert_called_once_with()

        with self.assertRaises(TypeError):
            c.cache_path = sys.executable
        c.cache_path = tempfile.gettempdir()
        with mock.patch('src.sig.base_custom_signal.CustomSignal.send') as m:
            c.saved_games_path = tempfile.mkdtemp()
            m.assert_called_once_with()




