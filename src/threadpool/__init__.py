# coding=utf-8

from src.low.custom_logging import make_logger
from src.threadpool.threadpool import ThreadPool

threadpool_seq = ThreadPool(_num_threads=1, _basename='sequential_pool', _daemon=True)
threadpool_par = ThreadPool(_num_threads=32, _basename='parallel_pool', _daemon=True)
threadpool_sta = ThreadPool(_num_threads=1, _basename='startup_tasks', _daemon=True)
threadpool_sig = ThreadPool(_num_threads=1, _basename='sig_pool', _daemon=True)


def join_all():
    logger = make_logger(__name__)
    logger.critical('joining all thread pools')
    for pool in [threadpool_sta, threadpool_par, threadpool_seq]:
        pool.join_all()


def kill_all():
    logger = make_logger(__name__)
    logger.critical('killing all thread pools')
    for pool in [threadpool_sta, threadpool_par, threadpool_seq]:
        pool.join_all(False, False)
