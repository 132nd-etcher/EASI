# coding=utf-8
from blinker_herald import emit

from src.low import constants
from src.low.custom_logging import make_logger

logger = make_logger(__name__)


@emit(sender=lambda func: func.__name__)
def init_modules():
    """
    This should be run in a thread with QtApp started
    """
    logger.info('INIT: start')
    import os
    if not os.getenv('APPVEYOR'):
        from src.upd import check_for_update
        check_for_update()
    from src.dcs.dcs_installs import init_dcs_installs
    init_dcs_installs()
    from src.keyring.keyring import init_keyring
    init_keyring()
    from src.rem import init_remotes
    init_remotes()
    if constants.TESTING:
        logger.debug('testing mode, skipping helpers download & cache init')
    else:
        from src.helper import init_helpers
        init_helpers()
    from src.cache.cache import init_cache
    init_cache()
    # from src.mod.local_mod import init_local_mods
    # init_local_mods()
    from src.repo.repo_local import init_local_meta_repo
    init_local_meta_repo()

    from src.mod.mod_creator import init_mod_creator
    init_mod_creator()

    logger.info('INIT: done')
