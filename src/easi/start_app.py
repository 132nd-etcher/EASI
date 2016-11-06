# coding=utf-8
import sys

from blinker_herald import emit

from src.easi.init_modules import init_modules
from src.low import constants
from src.low.custom_logging import make_logger

logger = make_logger(__name__)


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
