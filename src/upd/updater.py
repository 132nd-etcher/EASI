# coding=utf-8

from src.__version__ import __version__
from src.cfg import config
from src.low import constants
from src.low.custom_logging import make_logger
from src.low.version import Version
from src.rem.gh import GHLatest
from src.sig import sig_main_ui_states

logger = make_logger(__name__)


def install_new_version(latest_version: GHLatest):
    raise NotImplementedError


def get_latest_version(gh_user: str, gh_repo: str) -> GHLatest or None:
    logger.debug('getting latest version from: {}/{}'.format(gh_user, gh_repo))
    try:
        latest = GHLatest(gh_user, gh_repo)
    except ConnectionError:
        logger.error('no online version found at all!')
        return None
    return latest


def check_for_update():
    logger.info('running')
    sig_main_ui_states.updater_started()
    local_version = Version(__version__)
    if config.subscribe_to_test_versions:
        logger.debug('looking for a newer test version')
        latest_test = get_latest_version(constants.GH_APP_USER, constants.GH_APP_REPO_TEST)
        if latest_test:
            if latest_test.version > local_version:
                logger.info('new TEST version found')
                install_new_version(latest_test)
            elif latest_test.version == local_version:
                logger.info('already running latest test version')
            else:
                logger.info('online version is older, skipping update')
    sig_main_ui_states.set_progress(50)
    latest = get_latest_version(constants.GH_APP_USER, constants.GH_APP_REPO)
    if latest:
        if latest.version > local_version:
            logger.info('new version found')
            install_new_version(latest)
        elif local_version == latest.version:
            logger.debug('already up-to-date')
        elif local_version > latest.version:
            latest.print_all()
            print(latest.version)
            logger.info('running experimental version of {}'.format(constants.APP_SHORT_NAME))
    sig_main_ui_states.updater_finished()
    logger.info('done')
