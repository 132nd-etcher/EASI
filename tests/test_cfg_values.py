# coding=utf-8

import sys
import tempfile
from unittest import mock

import pytest
from blinker import signal
from hypothesis import strategies as st, given

from tests.utils import ContainedTestCase


@given(x=st.one_of(st.booleans(), st.floats(), st.none(), st.integers()))
def test_type_error(config, x):
    with pytest.raises(TypeError):
        config.saved_games_path = x


def test_config_values(config, tmpdir):
    f = str(tmpdir.join('f'))
    with open(f, 'w') as _f:
        _f.write('')
    with pytest.raises(TypeError):
        config.saved_games_path = f
    with pytest.raises(FileNotFoundError):
        config.saved_games_path = ''

    def dummy(*args, **kwargs):
        print(args, kwargs)

    sig = signal('Config_saved_games_path_value_changed')
    m = mock.MagicMock(spec=dummy)
    sig.connect(m)
    config.saved_games_path = tempfile.gettempdir()
    m.assert_called_once_with('Config', value=tempfile.gettempdir())

    with pytest.raises(TypeError):
        config.cache_path = sys.executable
    config.cache_path = tempfile.gettempdir()