# coding=utf-8

from src.abstract import AbstractModMetaFull, AbstractMod
from src.mod.meta import ModDraftMeta
from src.ui import MsgDialog


class ModDraft(AbstractMod):
    def __init__(self):
        AbstractMod.__init__(self)
        self.__meta = ModDraftMeta()

    @property
    def meta(self) -> AbstractModMetaFull:
        return self.__meta

    @staticmethod
    def is_ready():
        return False

    def write(self):
        if not self.is_ready():
            MsgDialog.make('Missing fields: ', 'Oops')
            return
        else:
            self.__meta.write()
