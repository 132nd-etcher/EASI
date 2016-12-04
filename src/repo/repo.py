# coding=utf-8

from blinker_herald import signals
from send2trash import send2trash
from shortuuid import uuid

from src.cache.cache import Cache
from src.cache.cache_event import CacheEvent
from src.git.wrapper import GitRepository
from src.low.custom_path import Path
from src.low.custom_logging import make_logger
from src.mod.mod import Mod
from src.rem.gh.gh_anon import GHRepo
from src.rem.gh.gh_session import GHSession
from src.sig import SIG_LOCAL_MOD_CHANGED


logger = make_logger(__name__)


class Repo:
    def __init__(self, user: str):
        logger.info('init meta repo for user: {}'.format(user))

        self.__user = user

        if user == GHSession().user:
            logger.debug('valid GHSession found')
            self.__remote = GHSession().own_meta_repo
        else:
            try:
                self.__remote = GHSession().get_repo('EASIMETA', user=user)
            except FileNotFoundError:
                logger.error('user {} has not EASIMETA repository'.format(user))
                raise

        logger.debug('creating local GitRepository object')
        self.__local_git_repo = GitRepository(self.local_git_repo_path, auto_init=False)

        if not self.local.is_init:
            logger.debug('no local repo, cloning remote')
            self.__create_local_git_repo(user)
        else:
            ahead, behind = self.local.ahead_behind()
            logger.debug('local repo exists; behind: {} ahead: {}'.format(behind, ahead))
            if behind:
                logger.debug('local repo is behind remote, pulling')
                self.local.pull()

        self.__gather_local_mods()

        # noinspection PyUnusedLocal
        @signals.post_cache_changed_event.connect_via('Cache')
        def cache_signal_handler(sender, signal_emitter, event: CacheEvent):
            if str(event.src.abspath()).startswith(str(self.local_git_repo_path.abspath())):
                if event.src.isfile():
                    self.refresh_mods()

        self.cache_signal_handler = cache_signal_handler

        # noinspection PyUnusedLocal
        @signals.post_authenticate.connect_via('GHSession')
        def gh_user_changed(sender, *args, **kwargs):
            try:
                gh_session = kwargs['gh_session']
                assert isinstance(gh_session, GHSession)
                self.__remote = gh_session.get_repo('EASIMETA', user=self.__user)
            except FileNotFoundError:
                logger.error('user {} has not EASIMETA repository'.format(self.__user))

        self.gh_user_changed = gh_user_changed

    def __create_local_git_repo(self, user):
        self.local.clone_from('https://github.com/{}/EASIMETA.git'.format(user))

    def __gather_local_mods(self):
        """Refreshes the local mod dictionary"""
        self.__mods = {}
        for mod_meta_path in self.local_git_repo_path.listdir(pattern='*.yml'):
            mod = Mod(mod_meta_path, self)
            self.__mods[mod.meta.name] = mod

    def refresh_mods(self):
        self.__gather_local_mods()
        SIG_LOCAL_MOD_CHANGED.send()

    @property
    def github_url(self):
        return 'https://github.com/{}/EASIMETA.git'.format(self.user_name)

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
        mod = Mod(self.local_git_repo_path.joinpath('{}.yml'.format(mod_name)), self)
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
    def local(self) -> GitRepository:
        return self.__local_git_repo

    @property
    def remote(self) -> GHRepo:
        return self.__remote

    @property
    def user_name(self):
        return self.__user

    @property
    def mods(self):
        return set(self.__mods.values())

    @property
    def local_git_repo_path(self) -> Path:
        return Cache().meta_repos_folder.joinpath(self.user_name)

    @property
    def name(self) -> str:
        return str(self.local_git_repo_path.basename())

    @property
    def has_changed(self):
        return len(self.local.status) > 0

    @property
    def push_perm(self) -> bool:
        try:
            return self.remote.permissions().push
        except KeyError:
            return False
        except AttributeError:
            return False

    @property
    def owner(self):
        try:
            return self.remote.owner().login
        except KeyError:
            return False
