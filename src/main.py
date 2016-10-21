# coding=utf-8

import builtins
import os
import sys

from blinker import signal
from blinker_herald import emit

from src.low import constants
from src.low.custom_logging import make_logger
from src.low.custom_path import Path

if constants.TESTING:
    # Bypass creation of main logger for tests
    import logging

    logger = logging.getLogger('__main__')
else:
    logger = make_logger(log_file_path=constants.PATH_LOG_FILE)


def parse_args():
    from src.low import constants
    constants.ARGS = sys.argv
    if len(sys.argv) > 1:
        print('sys.argv: ', str(sys.argv))
        if 'test_and_exit' in sys.argv:
            constants.TESTING = True


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
    import certifi
    cacert = Path(certifi.where())
    logger.info('checking certificate')
    # noinspection SpellCheckingInspection
    if not cacert.crc32() == '5630AEBB':
        raise ImportError('cacert.pem file is corrupted, please reinstall EASI ({})'.format(cacert.crc32()))
    logger.debug('setting up local cacert file to: {}'.format(str(cacert)))
    import os
    os.environ['REQUESTS_CA_BUNDLE'] = str(cacert)


def init_sentry():
    from src.cfg.cfg import config
    logger.info('sentry: initializing')
    from src.sentry import crash_reporter
    logger.debug('sentry online: {}'.format(crash_reporter.state.ONLINE))
    crash_reporter.register_context('config', config)


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
    from PyQt5.QtWidgets import QApplication
    from src.ui.main_ui.main_ui import MainUi
    from src.ui.dialog_disclaimer.dialog import DisclaimerDialog

    logger.info('QApplication: starting')
    constants.QT_APP = QApplication([])
    # set_app_wide_font()
    logger.info('QApplication: started')
    constants.MAIN_UI = MainUi(constants.QT_APP)


def show_disclaimer():
    if constants.TESTING:
        logger.info('disclaimer: skipping (testing mode)')
    else:
        from src.cfg.cfg import config
        from src.ui.dialog_disclaimer.dialog import DisclaimerDialog
        logger.info('disclaimer: showing')
        if not DisclaimerDialog.make():
            logger.warning('disclaimer: user declined')
            sys.exit(0)
        if config.author_mode and not DisclaimerDialog.make_for_mod_authors():
            config.author_mode = False
        logger.info('disclaimer: done')


@emit(sender=lambda func: func.__name__)
def init_modules():
    """
    This should be run in a thread with QtApp started
    """
    from src.upd import check_for_update
    from src.keyring import init_keyring
    from src.dcs import init_dcs_installs
    from src.rem import init_remotes
    from src.helper import init_helpers
    if not os.getenv('APPVEYOR'):
        check_for_update()
    init_dcs_installs()
    init_keyring()
    init_remotes()
    if constants.TESTING:
        logger.debug('testing mode, skipping helpers download')
    else:
        init_helpers()


def start_app():
    from src.threadpool import ThreadPool
    import src.sig
    logger.info('startup: init modules: start')
    pool = ThreadPool(_num_threads=1, _basename='startup', _daemon=False)
    # signal(src.new_sig.SIG_INIT_MODULES_INTERRUPT).connect(pool.join_all)
    pool.queue_task(init_modules)
    logger.info('startup: init modules: done')

    if constants.TESTING or 'test_and_exit' in sys.argv:
        pool.join_all()
        constants.MAIN_UI.exit()
        sys.exit(0)
    else:
        logger.info('transferring control to QtApp')
        sys.exit(constants.QT_APP.exec())


def main():
    try:
        parse_args()
        replace_builtins()
        check_cert()
        init_sentry()
        init_qt_app()
        show_disclaimer()
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


if __name__ == '__main__':
    def nice_exit(*_):
        import os
        # Shameful monkey-patching to bypass windows being a jerk
        # noinspection PyProtectedMember
        os._exit(0)


    import signal as core_sig

    print('connecting SIGINT')
    core_sig.signal(core_sig.SIGINT, nice_exit)

    main()
