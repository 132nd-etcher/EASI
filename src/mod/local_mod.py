# coding=utf-8
import typing

from src.cache.cache import Cache
from src.low.singleton import Singleton
from src.mod.mod_objects.mod_draft import ModDraft


class LocalMod(metaclass=Singleton):
    def __init__(self):
        pass

    @staticmethod
    def drafts() -> typing.List[ModDraft]:
        return [ModDraft(x.basename()) for x in Cache().own_draft_mod_folder.listdir()]

    @staticmethod
    def mod_name_is_available(name: str, uuid: str) -> bool:
        for mod_draft in LocalMod.drafts():
            if mod_draft.name == name and mod_draft.uuid != uuid:
                return False
        return True
