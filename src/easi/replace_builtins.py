# coding=utf-8
import builtins
from src.low import constants
from src.low.custom_logging import make_logger

logger = make_logger(__name__)


def replace_builtins():
    logger.info('builtins overloads: registering')

    if constants.FROZEN:
        # noinspection PyUnusedLocal
        def new_print(*args, **kwargs):
            """Replace print builtins to mute output on frozen version"""
            logger.debug(' '.join([x for x in list(args) + list(kwargs.values()) if isinstance(x, str)]))

        builtins.print = new_print

    logger.info('builtins overloads: registered')
