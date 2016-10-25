# coding=utf-8
import os
from shortuuid import uuid
from src.dcs.dcs_installs import DCSInstalls
from src.cfg.cfg import Config
from src.low.custom_logging import make_logger
from src.low.custom_path import Path
from src.meta.meta import Meta
from src.meta.meta_property import MetaProperty

logger = make_logger(__name__)


class UnknownDestination(Exception):
    """"""


class SrcModFile:

    # noinspection SpellCheckingInspection
    known_destinations = dict(
        saved_games=['sg', 'saved games', 'saved_games', 'savedgames']
    )

    special_files_handlers = {
        'autoexec.cfg': None,
        'description.lua': None
    }

    def __init__(self, src, root):
        assert isinstance(src, Path)
        self.__path = src
        self.__dest, self.__relpath = self.verify_destination(root)

    @property
    def path(self) -> Path:
        return self.__path

    @property
    def dest(self) -> str:
        return self.__dest

    @property
    def relpath(self):
        return self.__relpath

    @property
    def filename(self):
        return self.path.basename()

    def __str__(self):
        return '{}: {} -> {} ({})'.format(self.filename, self.path.abspath(), self.dest, self.relpath)

    def verify_destination(self, root):
        destination = self.path.relpath(root)
        for known_destination, acceptable_values in self.known_destinations.items():
            if destination.lower().split('\\')[0] in acceptable_values:
                return known_destination, destination.lower().replace(destination.lower().split('\\')[0], '')
        raise UnknownDestination(destination)


class ModMeta(Meta):

    def __init__(self, path, _uuid=None, init_dict=None, auto_read=True):
        Meta.__init__(self, path=path, init_dict=init_dict, auto_read=auto_read)
        if _uuid is None:
            _uuid = uuid()
        self.uuid = _uuid

    @MetaProperty(None, str)
    def uuid(self, value: str):
        """"""

    @MetaProperty(None, str)
    def name(self, value: str):
        """"""


def discover_files(folder):
    out = []
    for root, _, files in os.walk(folder):
        for file in files:
            p = Path(os.path.join(root, file))
            out.append(SrcModFile(p, folder))

    return out


def parse_local_folder_into_mod_metadata(folder):
    dcs_install_dir, _, _ = getattr(DCSInstalls(), Config().active_dcs_installation)
    d = {'known_assets': [os.path.basename(x) for x in Path(dcs_install_dir).joinpath('Bazar/Liveries').listdir()]}
    print(d)
    files = discover_files(folder)
    print(files)
    for file in files:
        print(str(file))
    #     print(str(file.abspath()))


if __name__ == '__main__':
    DCSInstalls().discover_dcs_installation()
    parse_local_folder_into_mod_metadata(r'F:\DEV\EASI\EASIv0.0.11\tests\mod\dummy1')
    meta_mod = ModMeta('./test')
    print(meta_mod.uuid)
