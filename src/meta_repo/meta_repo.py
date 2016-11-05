# coding=utf-8

from shortuuid import uuid

from src.cache.cache import Cache
from src.git.wrapper import Repository
from src.low.custom_path import Path
from src.mod.mod import Mod
from src.rem.gh.gh_anon import GHRepo
from src.rem.gh.gh_session import GHSession
from src.sig import SIG_LOCAL_MOD_CHANGED


class MetaRepo:
    def __init__(self, user: str):
        self.__remote = GHSession().get_repo('EASIMETA', user=user)
        self.__local = Repository(Cache().meta_repos_folder.joinpath(user), auto_init=False)
        if not self.local.is_init:
            self.local.clone_from('https://github.com/{}/EASIMETA.git'.format(user))
        else:
            self.local.pull()
        self.__mods = {}
        for mod_meta_path in self.path.listdir(pattern='*.yml'):
            mod = Mod(mod_meta_path, self)
            self.__mods[mod.meta.name] = mod

    @property
    def github_url(self):
        return 'https://github.com/{}/EASIMETA.git'.format(self.name)

    def mod_name_is_available(self, mod_name: str, mod: Mod or None) -> bool:
        for other_mod in self.mods:
            if mod_name == other_mod.meta.name:
                if mod is None:
                    return False
                elif mod.meta.uuid != other_mod.meta.uuid:
                    return False
        return True

    def create_new_mod(self, mod_name: str):
        if mod_name in [mod.meta.name for mod in self.mods]:
            raise ValueError('mod already exists: {}'.format(mod_name))
        if not mod_name:
            raise ValueError('empty mod name')
        if GHSession().status in [False, None]:
            raise RuntimeError('no valid GHSession')
        mod = Mod(self.path.joinpath('{}.yml'.format(mod_name)), self, new_mod_name=mod_name)
        mod.meta.uuid = uuid()
        mod.meta.name = mod_name
        mod.meta.author = GHSession().status
        mod.meta.write()
        self.__mods[mod_name] = mod
        SIG_LOCAL_MOD_CHANGED.send()
        return mod

    @property
    def mods(self):
        return set(self.__mods.values())

    @property
    def local(self) -> Repository:
        return self.__local

    @property
    def remote(self) -> GHRepo:
        return self.__remote

    @property
    def path(self) -> Path:
        return self.__local.path

    @property
    def name(self) -> str:
        return str(self.path.basename())

    @property
    def has_changed(self):
        return len(self.local.status) > 0

    @property
    def push_perm(self) -> bool:
        try:
            return self.remote.permissions().push
        except KeyError:
            return False

    @property
    def owner(self):
        return self.remote.owner().login
