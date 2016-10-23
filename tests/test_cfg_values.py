# coding=utf-8

import sys
from unittest import mock

import pytest
from blinker import signal
from hypothesis import strategies as st, given


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
    td = str(tmpdir.mkdir('sub'))
    config.saved_games_path = td
    m.assert_called_once_with('Config', value=td)

    with pytest.raises(TypeError):
        config.cache_path = sys.executable
    config.cache_path = td
