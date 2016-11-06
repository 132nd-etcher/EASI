# coding=utf-8
from send2trash import send2trash
from src.low.custom_logging import make_logger

logger = make_logger(__name__)


def delete_pending():
    logger.info('processing')
    from src.cfg.cfg import Config
    to_del = set(Config().to_del)
    while to_del:
        from src.low.custom_path import Path
        assert isinstance(to_del, set)
        path = str(Path(to_del.pop()).abspath())
        logger.debug('removing: {}'.format(path))
        send2trash(path)
    Config().to_del = to_del
    logger.info('done')