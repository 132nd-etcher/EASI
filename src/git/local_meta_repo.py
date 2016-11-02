# coding=utf-8


from src.cache.cache import Cache
from src.git.meta_repo import MetaRepo
from src.low.constants import EASIMETA_REPO_URL
from src.low.custom_logging import make_logger
from src.low.singleton import Singleton
from src.rem.gh.gh_session import GHSession

logger = make_logger(__name__)


class LocalMetaRepo(metaclass=Singleton):
    def __init__(self):
        self.__repos = {}
        for repo in Cache().meta_repos_folder.listdir():
            self.__repos[str(repo.basename())] = MetaRepo(repo)

        if 'EASIMETA' not in self.__repos:
            self.__repos['EASIMETA'] = MetaRepo.clone(
                EASIMETA_REPO_URL,
                self.main_easi_meta_repo_path,
            )

        if self.own_meta_repo_path:
            if GHSession().status not in self.__repos:
                self.__repos[GHSession().status] = MetaRepo.clone(
                    self.own_meta_repo_url,
                    self.own_meta_repo_path,
                )

    def __iter__(self) -> MetaRepo:
        for repo in self.__repos.values():
            yield repo

    def repo_names(self):
        return [repo_name for repo_name in self.__repos.keys()]

    @property
    def main_easi_meta_repo_path(self):
        return Cache().meta_repos_folder.joinpath('EASIMETA')

    @property
    def own_meta_repo_path(self):
        if self.own_meta_repo_name:
            return Cache().meta_repos_folder.joinpath(self.own_meta_repo_name)
        else:
            return None

    @property
    def own_meta_repo_name(self):
        if GHSession().status:
            return GHSession().status
        else:
            return None

    @property
    def own_meta_repo_url(self):
        if GHSession().status:
            return r'https://github.com/{}/EASIMETA.git'.format(GHSession().status)
        else:
            return None


def init_local_meta_repo():
    logger.info('initializing')
    LocalMetaRepo()
    logger.info('initialized')
