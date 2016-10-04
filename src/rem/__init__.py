# coding=utf-8

from src.keyring import keyring
from .gh.gh_session import GHSession
from .db.db_session import DBSession


def init_remotes():
    GHSession(keyring.gh_token)
    DBSession(keyring.db_token)
