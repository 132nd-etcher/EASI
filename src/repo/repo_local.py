# coding=utf-8


from src.cache.cache import Cache
from src.repo.repo import Repo
from src.low.custom_logging import make_logger
from src.low.singleton import Singleton
from src.rem.gh.gh_session import GHSession
from src.sig import SIG_LOCAL_REPO_CHANGED, SigProgress, SigMsg
from src.cfg.cfg import Config
from blinker_herald import signals, emit

logger = make_logger(__name__)


class LocalRepo(metaclass=Singleton):
    def __init__(self):
        self.__repos = {}

        self.__gather_local_repositories()

        self.__make_easi_root_repo()

        self.__make_own_repo()

        # noinspection PyUnusedLocal
        @signals.post_authenticate.connect_via('GHSession')
        def post_authenticate(sender, *args, **kwargs):
            gh_session = kwargs['gh_session']
            assert isinstance(gh_session, GHSession)
            self.__make_own_repo(gh_session)

        self.post_authenticate = post_authenticate

    def __gather_local_repositories(self):
        SigProgress().set_progress_title('Gathering local meta-repositories')
        SigProgress().set_progress(0)
        total = len(Cache().meta_repos_folder.listdir())
        current = 0
        for repo in Cache().meta_repos_folder.listdir():
            user_name = str(repo.basename())
            SigProgress().set_progress_text('Initializing meta-repository: {}'.format(user_name))
            self.__repos[user_name] = Repo(user_name)
            current += 1
            SigProgress().set_progress((current / total) * 100)

    def __make_easi_root_repo(self):
        logger.debug('looking for EASI root meta-repository')
        if 'EASIMETA' not in self.__repos:
            logger.debug('EASI root meta-repository not found, initializing')
            SigProgress().set_progress_text('Initializing EASI root meta-repository')
            SigProgress().set_progress(0)
            self.__repos['EASIMETA'] = Repo('EASIMETA')
            SigProgress().set_progress(100)
        else:
            logger.debug('EASI root meta-repository found')

    def __make_own_repo(self, gh_session: GHSession = None):
        if gh_session is None:
            gh_session = GHSession()

        logger.debug('looking for own meta repository')
        if gh_session.user and gh_session.user not in self.__repos:
            logger.debug('own meta-repository not found, initializing')
            SigProgress().set_progress_text('Initializing own meta-repository: {}'.format(gh_session.user))
            SigProgress().set_progress(0)
            self.add_repo(gh_session.user)
            SigProgress().set_progress(100)
            SIG_LOCAL_REPO_CHANGED.send('repo_local')
        else:
            logger.debug('own meta-repository found')

    def __getitem__(self, item) -> Repo:
        return self.__repos[item]

    @property
    def repos(self) -> list:
        return list(x for x in self.__repos.values())

    @property
    def names(self) -> list:
        return list(x for x in self.__repos.keys())

    @property
    def own_meta_repo(self) -> Repo or None:
        if GHSession().user:
            try:
                return self.__repos[GHSession().user]
            except KeyError:
                logger.exception('own repository not found')
        else:
            return None

    @property
    def root_meta_repo(self) -> Repo:
        return self.__repos['EASIMETA']

    @property
    def mods(self) -> list:
        return [mod for repo in self.__repos.values() for mod in repo.mods]

    @property
    def mod_names(self) -> list:
        return [mod.name for repo in self.__repos.values() for mod in repo.mods]

    @emit(only='post', capture_result=False, sender='LocalRepoUpdate')
    def add_repo(self, user_name: str):
        if user_name in self.__repos.keys():
            SigMsg().error('This repository has already been added')
            return
        try:
            repo = Repo(user_name)
        except FileNotFoundError:
            SigMsg().error('The repository was not found')
            return
        self.__repos[user_name] = repo
        if repo in Config().to_del:
            Config().to_del.remove(repo.local_git_repo_path.abspath())
        SIG_LOCAL_REPO_CHANGED.send('added repo: {}'.format(user_name))

    @emit(only='post', capture_result=False, sender='LocalRepoUpdate')
    def remove_repo(self, user_name: str):
        if user_name not in self.__repos.keys():
            raise ValueError('no repo for user "{}"'.format(user_name))
        repo = self.__repos[user_name]
        # send2trash(str(repo.path.abspath()))
        to_del = set(Config().to_del)
        to_del.add(str(repo.local_git_repo_path.abspath()))
        Config().to_del = to_del
        # repo.path.rmtree()
        del self.__repos[user_name]
        SIG_LOCAL_REPO_CHANGED.send('removed repo: {}'.format(user_name))


def init_local_meta_repo():
    logger.info('initializing')
    LocalRepo()
    logger.info('initialized')
