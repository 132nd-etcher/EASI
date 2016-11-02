# coding=utf-8

from src.keyring.keyring import Keyring
from src.sig import SigProgress
from .gh.gh_session import GHSession
from .db.db_session import DBSession
from src.low.custom_logging import make_logger


logger = make_logger(__name__)


def init_remotes():
    logger.info('initializing')
    SigProgress().set_progress(0)
    SigProgress().set_progress_text('Authenticating connected Github account')
    GHSession(Keyring().gh_token)
    SigProgress().set_progress(50)
    SigProgress().set_progress_text('Authenticating connected Dropbox account')
    DBSession(Keyring().db_token)
    SigProgress().set_progress(100)
    logger.info('initialized')
