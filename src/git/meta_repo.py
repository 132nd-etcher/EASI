# coding=utf-8

from src.git.wrapper import Repository
from src.low.custom_path import Path
from src.rem.gh.gh_session import GHSession


class MetaRepo(Repository):
    def __init__(self, path):
        path = Path(path)
        Repository.__init__(self, path, auto_init=False)
        self.__name = str(path.basename())
        self.__gh_repo = None

    @property
    def name(self):
        return self.__name

    @property
    def gh_repo(self):
        if self.__gh_repo is None:
            self.__gh_repo = GHSession().get_repo('EASIMETA', self.name)
        return self.__gh_repo

    @property
    def has_changed(self):
        print('has_changed', self.path)
        return len(self.status) > 0

    @property
    def push_perm(self) -> bool:
        return self.gh_repo.permissions().push

    @property
    def owner(self):
        return self.gh_repo.owner().login

    @staticmethod
    def clone(url, path, bare=False, repository=None, remote=None, checkout_branch='master', callbacks=None):
        Repository.clone(url, path, bare, repository, remote, checkout_branch, callbacks)
        return MetaRepo(path)
