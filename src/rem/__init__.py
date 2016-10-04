# coding=utf-8

from src.keyring import keyring
from .gh.gh_session import GHSession
from .db.db_session import DBSession


def init_remotes():
    gh_session = GHSession(keyring.gh_token)
    db_session = DBSession(keyring.db_token)
