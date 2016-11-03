# coding=utf-8

from src.git.wrapper import Repository
from src.low.custom_path import Path
from src.cache.cache import Cache
from src.rem.gh.gh_session import GHSession
from src.rem.gh.gh_anon import GHRepo
from src.mod.mod import Mod


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
