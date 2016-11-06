# coding=utf-8
import sys

from src.low import constants
from src.low.custom_logging import make_logger

logger = make_logger(__name__)


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
