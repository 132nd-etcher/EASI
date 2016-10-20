# coding=utf-8

import pytest
from src.low.singleton import Singleton
from src.cfg.cfg import Config
from src.rem.gh.gh_session import GHAnonymousSession


@pytest.fixture()
def config(tmpdir):
    Singleton.wipe_instances()
    # noinspection PyProtectedMember
    assert len(Singleton._instances) == 0
    p = str(tmpdir.join('c'))
    return Config(config_file_path=p)


@pytest.fixture(scope='session')
def gh_anon():
    return GHAnonymousSession()
