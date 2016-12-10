# coding=utf-8
from src.low.custom_logging import make_logger

logger = make_logger(__name__)


def init_sentry():
    logger.info('initializing')
    from src.cfg.cfg import Config
    from src.sentry.sentry import crash_reporter
    logger.debug('sentry online: {}'.format(crash_reporter.state.ONLINE))
    crash_reporter.register_context('config', Config())
    logger.info('initialized')
