# coding=utf-8
from src.low.custom_logging import make_logger

logger = make_logger(__name__)


def check_cert():
    logger.info('certificate: checking')
    import certifi
    import os

    from src.low.custom_path import Path
    cacert = Path(certifi.where())
    # noinspection SpellCheckingInspection
    if not cacert.crc32() == '5630AEBB':
        raise ImportError('cacert.pem file is corrupted, please reinstall EASI ({})'.format(cacert.crc32()))
    logger.debug('setting up local cacert file to: {}'.format(str(cacert)))
    os.environ['REQUESTS_CA_BUNDLE'] = str(cacert)
    logger.info('certificate: checked')
