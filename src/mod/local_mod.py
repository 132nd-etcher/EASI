# coding=utf-8
import typing

from src.cache.cache import Cache
from src.low.custom_logging import make_logger
from src.low.custom_path import Path
from src.low.singleton import Singleton
from src.mod.mod_objects.mod_draft import ModDraft

logger = make_logger(__name__)


class LocalMod(metaclass=Singleton):
    def __init__(self):
        pass

    @staticmethod
    def drafts() -> typing.List[ModDraft]:
        logger.debug('getting mod drafts')
        for x in Cache().own_mods_folder.listdir():
            if Path(x).isfile() and x.endswith('.easi_mod_draft'):
                try:
                    logger.debug('found draft in: {}'.format(x.basename().replace('.easi_mod_draft', '')))
                    yield ModDraft(x.basename().replace('.easi_mod_draft', ''))
                except TypeError:
                    pass

    @staticmethod
    def mod_name_is_available(name: str, uuid: str) -> bool:
        for mod_draft in LocalMod.drafts():
            if mod_draft.name == name and mod_draft.uuid != uuid:
                return False
        return True
