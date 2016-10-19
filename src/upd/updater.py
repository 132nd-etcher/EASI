# coding=utf-8
# noinspection PyProtectedMember
import semver
from src.__version__ import __version__
from src.cfg import config
from src.low import constants
from src.low.custom_logging import make_logger
from src.rem.gh.gh_session import GHAnonymousSession
from src.rem.gh.gh_objects.gh_release import GHRelease
from src.sig import sig_main_ui_states  # , sig_splash, sig_main_ui, sig_interrupt_startup

logger = make_logger(__name__)


# def install_new_version(gh_release: GHRelease):
#
#     # def run_setup(fdl: FileDownload):
#     #     if fdl.success:
#     #         sig_long_op_dialog.set_progress(100)
#     #         execl(fdl.local_file.abspath(), '/SP-', '/silent')
#     #         _exit(0)
#
#     sig_interrupt_startup.send()
#     sig_main_ui.hide()
#     sig_splash.kill()
#     # try:
#     #     setup_size = gh_release.assets()[0].size
#     # except IndexError:
#     #     logger.warning('no asset found for this release, it\'s probably still uploading; next time\'s the charm !')
#     # else:
#     #     sig_long_op_dialog.show('Updating EASI', 'Downloading setup ...')
#     #     # downloader.download(
#     #     #     gh_release.setup_download_url,
#     #     #     local_file=create_temp_file(suffix='.exe'),
#     #     #     progress=sig_long_op_dialog,
#     #     #     callback=run_setup,
#     #     #     size=setup_size)
#     #     # print(gh_release.setup_download_url)
#     #     # raise NotImplementedError  # FIXME


def check_if_new(gh_release: GHRelease):
    comp = semver.compare(gh_release.version, __version__) == 1
    if comp == 1:
        logger.info('new version found')
        # install_new_version(gh_release)
    elif comp == 0:
        logger.info('already running latest test version')
    else:
        logger.info('online version is older, skipping update')


def look_for_test_version(all_releases):
    for gh_release in all_releases.prerelease_only():
        check_if_new(gh_release)


def look_for_regular_version(all_releases):
    for gh_release in all_releases.final_only():
        check_if_new(gh_release)


def check_for_update():
    logger.info('running')
    sig_main_ui_states.set_progress_text('Looking for a newer version of {}'.format(constants.APP_SHORT_NAME))
    all_releases = GHAnonymousSession().get_all_releases(constants.GH_APP_USER, constants.GH_APP_REPO)
    if config.subscribe_to_test_versions:
        logger.debug('looking for a newer test version')
        look_for_test_version(all_releases)
    look_for_regular_version(all_releases)
    sig_main_ui_states.set_progress(50)
    sig_main_ui_states.set_progress(100)
    logger.info('done')
