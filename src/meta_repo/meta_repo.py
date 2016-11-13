# coding=utf-8

from blinker_herald import signals
from send2trash import send2trash
from shortuuid import uuid

from src.cache.cache import Cache
from src.cache.cache_event import CacheEvent
from src.git.wrapper import Repository
from src.low.custom_path import Path
from src.low.custom_logging import make_logger
from src.mod.mod import Mod
from src.rem.gh.gh_anon import GHRepo
from src.rem.gh.gh_session import GHSession
from src.sig import SIG_LOCAL_MOD_CHANGED


logger = make_logger(__name__)


class MetaRepo:
    def __init__(self, user: str):
        logger.info('creating meta repo for user: {}'.format(user))
        self.__remote = GHSession().get_repo('EASIMETA', user=user)
        self.__local = Repository(Cache().meta_repos_folder.joinpath(user), auto_init=False)
        if not self.local.is_init:
            logger.debug('no local repo, cloning remote')
            self.local.clone_from('https://github.com/{}/EASIMETA.git'.format(user))
        else:
            ahead, behind = self.local.ahead_behind()
            if behind:
                logger.debug('local repo is behind remote, pulling')
                self.local.pull()
        self.__mods = {}
        for mod_meta_path in self.path.listdir(pattern='*.yml'):
            mod = Mod(mod_meta_path, self)
            self.__mods[mod.meta.name] = mod

        # noinspection PyUnusedLocal
        def cache_signal_handler(sender, signal_emitter, event: CacheEvent):
            if str(event.src.abspath()).startswith(str(self.path.abspath())):
                if event.src.isfile():
                    self.refresh_mods()

        self.cache_signal_handler = cache_signal_handler

        signals.post_cache_changed_event.connect(self.cache_signal_handler, weak=False)

    def refresh_mods(self):
        self.__mods = {}
        for mod_meta_path in self.path.listdir(pattern='*.yml'):
            mod = Mod(mod_meta_path, self)
            self.__mods[mod.meta.name] = mod
        SIG_LOCAL_MOD_CHANGED.send()

    @property
    def github_url(self):
        return 'https://github.com/{}/EASIMETA.git'.format(self.name)

    def mod_name_is_available(self, mod_name: str, mod: Mod or None) -> bool:
        for other_mod in self.mods:
            if mod_name == other_mod.meta.name:
                if mod is None or mod.meta.uuid != other_mod.meta.uuid:
                    logger.debug('name is *not* available')
                    return False
        return True

    def mod_name_is_available_new(self, mod_name: str) -> bool:
        for other_mod in self.mods:
            if mod_name == other_mod.meta.name:
                return False
        return True

    def create_new_mod(self, mod_name: str):
        logger.debug('creating new mod')
        if not mod_name:
            raise ValueError('empty mod name')
        if mod_name in [mod.meta.name for mod in self.mods]:
            raise ValueError('mod already exists: {}'.format(mod_name))
        if GHSession().user in [False, None]:
            raise RuntimeError('no valid GHSession')
        mod = Mod(self.path.joinpath('{}.yml'.format(mod_name)), self)
        mod.meta.uuid = uuid()
        mod.meta.name = mod_name
        mod.meta.author = GHSession().user
        mod.meta.write()
        self.__mods[mod_name] = mod
        SIG_LOCAL_MOD_CHANGED.send()
        logger.debug('creation ok')
        return mod

    def trash_mod(self, mod_name: str):
        logger.debug('trashing mod')
        signals.post_cache_changed_event.disconnect(self.cache_signal_handler)
        if not mod_name:
            raise ValueError('empty mod name')
        if mod_name not in [mod.meta.name for mod in self.mods]:
            raise ValueError('no mod named: {}'.format(mod_name))
        mod = self.__mods[mod_name]
        assert isinstance(mod, Mod)
        if mod.local_folder.exists():
            send2trash(str(mod.local_folder.abspath()))
        send2trash(str(mod.meta.path.abspath()))
        # to_del = set(Config().to_del)
        # to_del.add(str(mod.repo.path.abspath()))
        # Config().to_del = to_del
        del self.__mods[mod_name]
        SIG_LOCAL_MOD_CHANGED.send()
        signals.post_cache_changed_event.connect(self.cache_signal_handler, weak=False)

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
        try:
            return self.remote.owner().login
        except KeyError:
            return False
