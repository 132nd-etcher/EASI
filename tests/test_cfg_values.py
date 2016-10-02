# coding=utf-8

import tempfile
import sys
from unittest import mock

from hypothesis import strategies as st, given

from src.cfg.values import ConfigValues
from src.low.meta import Meta
from tests.with_file import TestCaseWithTestFile


class C(Meta, ConfigValues):
    pass


class TestConfigValues(TestCaseWithTestFile):

    def setUp(self):
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
            c.cache = sys.executable
        with self.assertRaises(ValueError):
            c.cache = tempfile.gettempdir()
        with mock.patch('src.sig.base_custom_signal.CustomSignal.send') as m:
            c.saved_games_path = tempfile.mkdtemp()
            m.assert_called_once_with()




