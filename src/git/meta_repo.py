# coding=utf-8

from src.git.wrapper import Repository


class MetaRepo(Repository):
    def __init__(self, path):
        self.__repo = Repository.__init__(self, path, auto_init=False)

    @staticmethod
    def clone(url, path, bare=False, repository=None, remote=None, checkout_branch='master', callbacks=None):
        Repository.clone(url, path, bare, repository, remote, checkout_branch, callbacks)
        return MetaRepo(path)
