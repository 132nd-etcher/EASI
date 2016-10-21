# coding=utf-8

import pytest
from src.low.singleton import Singleton
from src.cfg.cfg import Config
from src.rem.gh.gh_session import GHAnonymousSession


@pytest.fixture()
def somefile(tmpdir_factory):
    """Returns an existing file"""
    p = str(tmpdir_factory.mktemp('some_dir', True).join('some_file'))
    with open(p, 'w') as f:
        f.write('')
    return p


@pytest.fixture()
def config(tmpdir):
    """Creates a new instance of src.cfg.cfg.Config object"""
    Singleton.wipe_instances()
    # noinspection PyProtectedMember
    assert len(Singleton._instances) == 0
    p = str(tmpdir.join('c'))
    return Config(config_file_path=p)


@pytest.fixture(scope='session')
def gh_anon():
    """Returns the Github anonymous request session"""
    return GHAnonymousSession()
