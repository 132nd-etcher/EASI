# coding=utf-8

from src.__version__ import version as local_version
from src.cfg import config
from src.low import constants
from src.low.custom_logging import make_logger
from src.rem.gh import GHAnonymousSession, GHSessionError
from src.rem.gh.gh_objects import GHRelease
from src.sig import sig_main_ui_states

logger = make_logger(__name__)


def install_new_version(latest_version: GHRelease):
    raise NotImplementedError  # FIXME


def local_version_is_older(online_version):
    if online_version > local_version:
        logger.info('new TEST version found')
    elif online_version == local_version:
        logger.info('already running latest test version')
    else:
        logger.info('online version is older, skipping update')


def look_for_online_version(gh_user, gh_repo):
    try:
        latest = GHAnonymousSession().get_latest_release(gh_user, gh_repo)
    except GHSessionError as e:
        logger.warning(e.msg)
    else:
        if latest:
            if local_version_is_older(latest.version):
                install_new_version(latest)


def look_for_test_version():
    look_for_online_version(constants.GH_APP_USER, constants.GH_APP_REPO_TEST)


def look_for_regular_version():
    look_for_online_version(constants.GH_APP_USER, constants.GH_APP_REPO)


def check_for_update():
    logger.info('running')
    sig_main_ui_states.set_progress_text('Looking for a newer version of {}'.format(constants.APP_SHORT_NAME))
    if config.subscribe_to_test_versions:
        logger.debug('looking for a newer test version')
        look_for_test_version()
    look_for_regular_version()
    sig_main_ui_states.set_progress(50)
    sig_main_ui_states.set_progress(100)
    logger.info('done')
