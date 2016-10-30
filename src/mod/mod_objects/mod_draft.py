# coding=utf-8


from src.cache.cache import Cache
from src.meta.meta import Meta
from src.mod.mod_objects.mod_base import BaseMod
from send2trash import send2trash


class ModDraft(Meta, BaseMod):
    def trash(self):
        send2trash(self.path)
        send2trash(self.repo.path)

    @property
    def meta_header(self):
        return 'EASI_MOD_DRAFT'

    def __init__(self, uuid):
        Meta.__init__(self, path=Cache().own_mods_folder.joinpath('{}.easi_mod_draft'.format(uuid)))
        BaseMod.__init__(self, uuid)
        self.uuid = uuid

    @property
    def status(self):
        return 'draft'
