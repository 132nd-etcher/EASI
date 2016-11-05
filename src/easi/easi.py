# coding=utf-8

import builtins
import sys

from blinker_herald import emit

from src.low import constants
from src.low.custom_logging import make_logger

if len(sys.argv) > 1:
    print('sys.argv: ', str(sys.argv))
    if 'test_and_exit' in sys.argv:
        constants.TESTING = True
    if 'no_qt_app' in sys.argv:
        constants.QT_APP = False
constants.ARGS = [x for x in sys.argv]

if constants.TESTING:
    # Do not save log to file for test runs
    logger = make_logger('main')
    logger.info('logger initialized in testing mode')
else:
    logger = make_logger(log_file_path=constants.PATH_LOG_FILE)
    logger.info('logger initialized')


def replace_builtins():
    logger.info('builtins overloads: registering')

    if constants.FROZEN:
        # noinspection PyUnusedLocal
        def new_print(*args, **kwargs):
            """Replace print builtins to mute output on frozen version"""
            logger.debug(' '.join([x for x in list(args) + list(kwargs.values()) if isinstance(x, str)]))

        builtins.print = new_print

    logger.info('builtins overloads: registered')


def check_cert():
    logger.info('certificate: checking')
    import certifi
    import os

    from src.low.custom_path import Path
    cacert = Path(certifi.where())
    # noinspection SpellCheckingInspection
    if not cacert.crc32() == '5630AEBB':
        raise ImportError('cacert.pem file is corrupted, please reinstall EASI ({})'.format(cacert.crc32()))
    logger.debug('setting up local cacert file to: {}'.format(str(cacert)))
    os.environ['REQUESTS_CA_BUNDLE'] = str(cacert)
    logger.info('certificate: checked')


def init_sentry():
    logger.info('initializing')
    from src.cfg import Config
    from src.sentry import crash_reporter
    logger.debug('sentry online: {}'.format(crash_reporter.state.ONLINE))
    crash_reporter.register_context('config', Config())
    logger.info('initialized')


def set_app_wide_font():
    from PyQt5.QtGui import QFontDatabase
    from src.qt import qt_resources

    logger.info('QFontDatabase: starting')
    font_db = QFontDatabase()
    logger.debug('QFontDatabase: adding font to database')
    font_db.addApplicationFont(qt_resources.app_font)
    logger.debug('QFontDatabase: registering app-wide font')
    constants.QT_APP.setFont(font_db.font('Anonymous Pro', 'normal', 9))
    logger.info('QFontDatabase: started')


def init_qt_app():
    logger.info('initializing')
    from src.ui.main_ui import MainUi
    if constants.QT_APP is False:
        logger.warn('starting MainUI *without* a QtApp object')
        MainUi()
    else:
        from PyQt5.QtWidgets import QApplication
        logger.debug('starting QtApp object')
        constants.QT_APP = QApplication([])
        # set_app_wide_font()
        logger.debug('starting MainUI')
        MainUi()
        logger.info('initialized')
    from src.easi.gui_mode import connect_signals
    connect_signals()


def show_disclaimer():
    if constants.TESTING:
        logger.info('disclaimer: skipping (testing mode)')
    else:
        from src.cfg import Config
        from src.ui.dialog_disclaimer.dialog import DisclaimerDialog
        logger.info('disclaimer: showing')
        if not DisclaimerDialog.make():
            logger.warning('disclaimer: user declined')
            sys.exit(0)
        if Config().author_mode and not DisclaimerDialog.make_for_mod_authors():
            Config().author_mode = False
        logger.info('disclaimer: done')


def delete_pending():
    logger.info('processing')
    from src.cfg.cfg import Config
    to_del = Config().to_del
    while to_del:
        from src.low.custom_path import Path
        assert isinstance(to_del, set)
        path = Path(to_del.pop())
        logger.debug('removing: {}'.format(path.abspath()))
        if path.isdir():
            path.rmtree()
        elif path.isfile():
            path.remove()
    Config().to_del = to_del
    logger.info('done')


@emit(sender=lambda func: func.__name__)
def init_modules():
    """
    This should be run in a thread with QtApp started
    """
    logger.info('INIT: start')
    import os
    if not os.getenv('APPVEYOR'):
        from src.upd import check_for_update
        check_for_update()
    from src.dcs.dcs_installs import init_dcs_installs
    init_dcs_installs()
    from src.keyring.keyring import init_keyring
    init_keyring()
    from src.rem import init_remotes
    init_remotes()
    if constants.TESTING:
        logger.debug('testing mode, skipping helpers download & cache init')
    else:
        from src.helper import init_helpers
        init_helpers()
    from src.cache.cache import init_cache
    init_cache()
    # from src.mod.local_mod import init_local_mods
    # init_local_mods()
    from src.meta_repo.local_meta_repo import init_local_meta_repo
    init_local_meta_repo()
    logger.info('INIT: done')


@emit(sender='main')
def start_app():
    from src.threadpool import ThreadPool
    logger.info('fill starting pool: begin')
    pool = ThreadPool(_num_threads=1, _basename='startup', _daemon=False)
    # signal(src.new_sig.SIG_INIT_MODULES_INTERRUPT).connect(pool.join_all)
    pool.queue_task(init_modules)
    pool.queue_task(logger.info, ['all done'])
    logger.info('fill starting pool: done')

    if constants.TESTING:
        logger.info('TESTING mode: waiting for pool to join')
        pool.join_all()
        logger.info('TESTING mode: pool is done')
        if constants.QT_APP:
            logger.info('TESTING mode: closing QtApp')
            constants.QT_APP.exit(0)
        logger.info('start_app: TESTING mode: returning')
        return True
    else:
        logger.info('transferring control to QtApp')
        sys.exit(constants.QT_APP.exec())


def nice_exit(*_):
    import os
    # Shameful monkey-patching to bypass windows being a jerk
    # noinspection PyProtectedMember
    os._exit(0)


def start_gui():
    try:
        replace_builtins()
        check_cert()
        init_sentry()
        init_qt_app()
        show_disclaimer()
        delete_pending()
        start_app()

    except SystemExit:
        print('catched SystemExit')
        if constants.TESTING:
            return
        nice_exit(0, None)
    except KeyboardInterrupt:
        print('catched KeyboardInterrupt')
        if constants.TESTING:
            return
        nice_exit(0, None)
