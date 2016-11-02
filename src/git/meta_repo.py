# coding=utf-8

from src.git.wrapper import Repository
from src.low.custom_path import Path
from src.rem.gh.gh_session import GHSession


class MetaRepo(Repository):
    def __init__(self, path):
        path = Path(path)
        self.__repo = Repository.__init__(self, path, auto_init=False)
        self.__name = str(path.basename())
        self.__push_perm = None

    @property
    def push_perm(self) -> bool:
        if self.__push_perm is None:
            self.__push_perm = GHSession().get_repo('EASIMETA', self.name).permissions().push
        return self.__push_perm

    @property
    def name(self):
        return self.__name

    @staticmethod
    def clone(url, path, bare=False, repository=None, remote=None, checkout_branch='master', callbacks=None):
        Repository.clone(url, path, bare, repository, remote, checkout_branch, callbacks)
        return MetaRepo(path)
