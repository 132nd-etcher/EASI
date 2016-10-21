# coding=utf-8

import os
from unittest import skip

import pytest
from blinker import signal
from hypothesis import strategies as st, given


def test_config_init(config, tmpdir):
    assert config.path.abspath() == str(tmpdir.join('c'))


def test_signal(config, tmpdir, mocker):
    new_value = tmpdir.join('file')
    sig = signal('Config_cache_path_value_changed')
    spy = mocker.spy(sig, 'send')
    config.cache_path = str(new_value)
    spy.assert_called_with('Config', value=new_value)


@skip('works fine alone, not in bulk')
def test_set_path(config):
    assert not config.path.exists()
    # noinspection PyProtectedMember
    assert len(config.data) == 0
    config.subscribe_to_test_versions = True
    # noinspection PyProtectedMember
    assert len(config.data) > 0
    config.write()
    assert config.path.exists()


@given(x=st.one_of(st.booleans(), st.floats(), st.integers(), st.none(), st.sets(st.booleans())))
def test_type_str_enforcement(config, x):
    for val in {'active_dcs_installation', 'cache_path', 'kdiff_path', 'saved_games_path', 'usr_name', 'usr_email'}:
        with pytest.raises(TypeError):
            setattr(config, val, x)


@given(x=st.one_of(st.text(), st.floats(), st.integers(), st.none(), st.sets(st.booleans())))
def test_type_bool_enforcement(config, x):
    for val in {'author_mode', 'encrypt_keyring', 'subscribe_to_test_versions'}:
        with pytest.raises(TypeError):
            setattr(config, val, x)


def test_path_str_enforcement(config, tmpdir):
    p = str(tmpdir.join('d'))
    f = str(tmpdir.join('f'))
    k = str(tmpdir.join('kdiff3.exe'))
    with open(f, 'w') as _f:
        _f.write('')

    with pytest.raises(FileNotFoundError):
        config.saved_games_path = p
    with pytest.raises(TypeError):
        config.cache_path = f
    with pytest.raises(TypeError):
        config.cache_path = f
    assert not os.path.exists(p)
    config.cache_path = p
    assert os.path.exists(p)
    with pytest.raises(FileNotFoundError):
        config.kdiff_path = k
    with pytest.raises(ValueError):
        config.kdiff_path = p
    with pytest.raises(ValueError):
        config.kdiff_path = f
    with open(k, 'w') as _f:
        _f.write('')
    config.kdiff_path = k
