# coding=utf-8


from src.low.custom_logging import make_logger


logger = make_logger(__name__)


def init_helpers():
    logger.info('initializing')
    from .kdiff import kdiff
    if not kdiff.is_installed:
        kdiff.download_and_install()
    logger.info('initialized')
