# coding=utf-8

from src.keyring import keyring
from .gh.gh_session import GHSession


def init_remotes():
    gh_session = GHSession(keyring.gh_token)
