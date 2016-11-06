# coding=utf-8
from src.low.custom_logging import make_logger
from src.low import constants


logger = make_logger(__name__)


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