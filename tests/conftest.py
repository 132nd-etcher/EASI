# coding=utf-8

import pytest

from src.low.custom_logging import make_logger
from src.low.singleton import Singleton
from src.cache.cache import Cache


@pytest.fixture(scope='session')
def secret():
    try:
        from vault.secret import Secret
    except ImportError:
        from vault.empty_secret import Secret
        pytest.skip('missing secret')
    yield Secret


# @pytest.fixture()
# def wipe_cache():
#     Singleton.wipe_instances('Cache')
#     yield
#     Singleton.wipe_instances('Cache')


# noinspection PyUnusedLocal,PyShadowingNames
@pytest.fixture(autouse=True)
def make_tmp_cache(tmpdir, monkeypatch, mocker):
    import src.cache.cache
    monkeypatch.setattr(src.cache.cache, 'SigProgress', mocker.MagicMock())
    Singleton.wipe_instances('Cache')
    c = Cache(str(tmpdir))
    yield
    c.stop()


@pytest.fixture(scope='session', autouse=True)
def make_test_logger():
    """Creates main logger for tests output"""
    make_logger('__main__').info('test logger initialized')


@pytest.fixture(autouse=True)
def set_testing_mode(monkeypatch):
    """Sets global testing mode"""
    from src.low import constants
    monkeypatch.setattr(constants, 'TESTING', True)


@pytest.fixture()
def somefile(tmpdir_factory):
    """Returns an existing file"""
    p = str(tmpdir_factory.mktemp('some_dir', True).join('some_file'))
    with open(p, 'w') as f:
        f.write('')
    return p


@pytest.fixture(autouse=True)
def config(tmpdir):
    """Creates a new instance of src.cfg.cfg.Config object"""
    from src.cfg.cfg import Config
    from src.low.singleton import Singleton
    Singleton.wipe_instances('Config')
    # noinspection PyProtectedMember
    assert 'Config' not in Singleton._instances
    p = str(tmpdir.join('c'))
    return Config(config_file_path=p)


@pytest.fixture(scope='session')
def gh_anon():
    """Returns the Github anonymous request session"""
    from src.rem.gh.gh_anon import GHAnonymousSession
    return GHAnonymousSession()
