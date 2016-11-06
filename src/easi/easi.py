# coding=utf-8

import sys

from src.easi.check_cert import check_cert
from src.easi.delete_pending import delete_pending
from src.easi.ini_sentry import init_sentry
from src.easi.init_qt_app import init_qt_app
from src.easi.nice_exit import nice_exit
from src.easi.replace_builtins import replace_builtins
from src.easi.show_disclaimer import show_disclaimer
from src.easi.start_app import start_app
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
