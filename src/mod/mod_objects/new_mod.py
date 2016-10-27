# coding=utf-8
import os

from shortuuid import uuid

from src.low.custom_path import Path
from src.meta.meta import Meta
from src.meta.meta_property import MetaProperty
from src.mod.mod_objects.new_mod_file import SrcModFile


class NewMod(Meta):
    def __init__(self, meta_path, root_folder_path, _uuid=None, init_dict=None, auto_read=True):
        Meta.__init__(self, path=meta_path, init_dict=init_dict, auto_read=auto_read)
        if _uuid is None:
            _uuid = uuid()
        self.uuid = _uuid

    def discover_files(self, root_folder_path):
        out = []
        for root, _, files in os.walk(root_folder_path):
            for file in files:
                p = Path(os.path.join(root, file))
                out.append(SrcModFile(p, root_folder_path))
        return out

    @MetaProperty(None, str)
    def uuid(self, value: str):
        """"""

    @MetaProperty(None, str)
    def name(self, value: str):
        """"""

    @MetaProperty(dict(), dict)
    def files(self, value):
        """"""