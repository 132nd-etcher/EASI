# coding=utf-8


from src.cache.cache import Cache
from src.meta_repo.meta_repo import MetaRepo
from src.low.custom_logging import make_logger
from src.low.singleton import Singleton
from src.rem.gh.gh_session import GHSession
from src.sig import SIG_LOCAL_REPO_CHANGED, SigProgress
from src.cfg.cfg import Config
from blinker_herald import signals

logger = make_logger(__name__)


class LocalMetaRepo(metaclass=Singleton):
    def __init__(self):
        self.__repos = {}
        total = len(Cache().meta_repos_folder.listdir())
        current = 0
        SigProgress().set_progress_title('Initializing meta-repositories')
        SigProgress().set_progress(0)
        for repo in Cache().meta_repos_folder.listdir():
            user_name = str(repo.basename())
            SigProgress().set_progress_text('Initializing meta-repository: {}'.format(user_name))
            self.__repos[user_name] = MetaRepo(user_name)
            current += 1
            SigProgress().set_progress((current / total) * 100)

        if 'EASIMETA' not in self.__repos:
            SigProgress().set_progress_text('Initializing meta-repository: EASIMETA')
            SigProgress().set_progress(0)
            self.__repos['EASIMETA'] = MetaRepo('EASIMETA')
            SigProgress().set_progress(100)

        self.make_own_repo()

        # noinspection PyUnusedLocal
        def post_authenticate(sender, *args, **kwargs):
            if sender == 'GHSession':
                self.make_own_repo()

        signals.post_authenticate.connect(post_authenticate, weak=False)

    def make_own_repo(self):

        if GHSession().user and GHSession().user not in self.__repos:
            SigProgress().set_progress_text('Initializing meta-repository: {}'.format(GHSession().user))
            SigProgress().set_progress(0)
            self.__repos[GHSession().user] = MetaRepo(GHSession().user)
            SigProgress().set_progress(100)
            SIG_LOCAL_REPO_CHANGED.send()

    def __getitem__(self, item) -> MetaRepo:
        return self.__repos[item]

    @property
    def repos(self) -> list:
        return list(x for x in self.__repos.values())

    @property
    def names(self) -> list:
        return list(x for x in self.__repos.keys())

    @property
    def own_meta_repo(self) -> MetaRepo:
        if GHSession().user:
            return self.__repos[GHSession().user]
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
        repo = MetaRepo(user_name)
        self.__repos[user_name] = repo
        if repo in Config().to_del:
            Config().to_del.remove(repo.path.abspath())
        SIG_LOCAL_REPO_CHANGED.send()

    def remove_repo(self, user_name: str):
        print('remove_repo')
        if user_name not in self.__repos.keys():
            raise ValueError('no repo for user "{}"'.format(user_name))
        repo = self.__repos[user_name]
        # send2trash(str(repo.path.abspath()))
        to_del = set(Config().to_del)
        to_del.add(str(repo.path.abspath()))
        Config().to_del = to_del
        # repo.path.rmtree()
        del self.__repos[user_name]
        SIG_LOCAL_REPO_CHANGED.send()


def init_local_meta_repo():
    logger.info('initializing')
    LocalMetaRepo()
    logger.info('initialized')
