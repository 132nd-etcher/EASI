# coding=utf-8


from src.cache.cache import Cache
from src.meta_repo.meta_repo import MetaRepo
from src.low.custom_logging import make_logger
from src.low.singleton import Singleton
from src.rem.gh.gh_session import GHSession
from src.sig import SIG_LOCAL_REPO_CHANGED

logger = make_logger(__name__)


class LocalMetaRepo(metaclass=Singleton):
    def __init__(self):
        self.__repos = {}
        for repo in Cache().meta_repos_folder.listdir():
            user_name = str(repo.basename())
            self.__repos[user_name] = MetaRepo(user_name)

        if 'EASIMETA' not in self.__repos:
            self.__repos['EASIMETA'] = MetaRepo('EASIMETA')

        if GHSession().status and GHSession().status not in self.__repos:
            self.__repos[GHSession().status] = MetaRepo(GHSession().status)

    def __getitem__(self, item):
        return self.__repos[item]

    @property
    def repos(self) -> list:
        return list(x for x in self.__repos.values())

    @property
    def names(self) -> list:
        return list(x for x in self.__repos.keys())

    @property
    def own_meta_repo(self) -> MetaRepo:
        if GHSession().status:
            return self.__repos[GHSession().status]
        else:
            return None

    @property
    def root_meta_repo(self) -> MetaRepo:
        return self.__repos['EASIMETA']

    @property
    def mods(self) -> list:
        return [mod for repo in self.__repos.values() for mod in repo.mods]

    @property
    def mod_names(self) -> list:
        return [mod.name for repo in self.__repos.values() for mod in repo.mods]

    def add_repo(self, user_name: str):
        if user_name in self.__repos.keys():
            raise ValueError('repo already added')
        self.__repos[user_name] = MetaRepo(user_name)
        SIG_LOCAL_REPO_CHANGED.send()


def init_local_meta_repo():
    logger.info('initializing')
    LocalMetaRepo()
    logger.info('initialized')