# coding=utf-8

from shortuuid import uuid
from send2trash import send2trash
from src.low.singleton import Singleton
from src.mod.mod import Mod
from src.cache.cache import Cache
from src.low.custom_logging import make_logger
from src.sig import SIG_LOCAL_MOD_CHANGED
from src.git.local_meta_repo import LocalMetaRepo
from src.rem.gh.gh_session import GHSession

logger = make_logger(__name__)


class LocalMod(metaclass=Singleton):
    def __init__(self):
        self.__mods = {}
        try:
            for repo in LocalMetaRepo():
                for mod_meta_path in repo.path.listdir(pattern='*.yml'):
                    mod = Mod(mod_meta_path)
                    self[mod.meta.name] = mod
        except FileNotFoundError:
            pass

    def create_new_mod(self, mod_name: str):
        if mod_name in self:
            raise ValueError('mod already exists: {}'.format(mod_name))
        if not mod_name:
            raise ValueError('empty mod name')
        if GHSession().status in [False, None]:
            raise RuntimeError('no valid GHSession')
        mod = Mod(Cache().own_meta_repo_folder.joinpath('{}.yml'.format(mod_name)), delay_repo=True)
        mod.meta.uuid = uuid()
        mod.meta.name = mod_name
        mod.meta.meta_repo_name = LocalMetaRepo().own_meta_repo_name
        mod.meta.author = GHSession().status
        mod.meta.write()
        self[mod_name] = mod
        SIG_LOCAL_MOD_CHANGED.send()
        return mod

    def move_meta(self, mod_name: str, new_repo_name):
        mod = self[mod_name]
        new_meta_path = Cache().meta_repos_folder.joinpath(new_repo_name).joinpath('{}.yml'.format(mod_name))
        old_meta_path = mod.meta.path
        # mod.meta.path.copy(new_meta_path)
        mod.meta.path = new_meta_path
        # mod.meta_repo_name = new_repo_name
        # mod.meta.meta_repo_name = new_repo_name
        mod.meta.write()
        old_meta_path.remove()
        SIG_LOCAL_MOD_CHANGED.send()

    def trash_mod(self, mod_name: str):
        mod = self[mod_name]
        send2trash(mod.meta.path)
        send2trash(mod.repo.path)
        del self[mod_name]
        SIG_LOCAL_MOD_CHANGED.send()

    def __setitem__(self, key, value):
        self.__mods[key] = value

    def __delitem__(self, key):
        del self.__mods[key]

    def __contains__(self, mod_name) -> bool:
        return self.__mods.__contains__(mod_name)
        # return mod_name in self.__mods.keys()

    def __getitem__(self, mod_name: str) -> Mod:
        return self.__mods.__getitem__(mod_name)
        # if mod_name not in self.__mods.keys():
        #     mod = Mod.make_new_mod(mod_name)
        #     mod.meta.uuid = uuid()
        #     self.__mods[mod_name] = mod
        # return self.__mods[mod_name]

    def __iter__(self) -> Mod:
        for mod in self.__mods.values():
            yield mod

    def mod_name_is_available(self, mod_name: str, mod_instance: Mod):
        for mod in self:
            if mod.meta.name == mod_name and mod is not mod_instance:
                return False
        return True


def init_local_mods():
    logger.info('initializing')
    LocalMod()
    logger.info('initialized')
