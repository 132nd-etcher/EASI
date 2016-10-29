# coding=utf-8
import typing

from src.cache.cache import Cache
from src.low.singleton import Singleton
from src.mod.mod_objects.mod_draft import ModDraft
from src.low.custom_path import Path


class LocalMod(metaclass=Singleton):
    def __init__(self):
        pass

    @staticmethod
    def drafts() -> typing.List[ModDraft]:
        for x in Cache().own_mods_folder.listdir():
            if Path(x).isfile():
                try:
                    yield ModDraft(x.basename)
                except TypeError:
                    pass
        # return [ModDraft(x.basename()) for x in Cache().own_mods_folder.listdir() if Path(x).isfile()]

    @staticmethod
    def mod_name_is_available(name: str, uuid: str) -> bool:
        for mod_draft in LocalMod.drafts():
            if mod_draft.name == name and mod_draft.uuid != uuid:
                return False
        return True
