# coding=utf-8

import sys

from blinker_herald import emit

from src.easi.check_cert import check_cert
from src.easi.delete_pending import delete_pending
from src.easi.ini_sentry import init_sentry
from src.easi.init_modules import init_modules
from src.easi.init_qt_app import init_qt_app
from src.easi.replace_builtins import replace_builtins
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
