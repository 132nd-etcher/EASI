# coding=utf-8

import os

import pygit2
from pygit2 import Signature

from src.low.custom_path import Path
from src.rem.gh import GHSession


class Repository:

    repo_status_map = {
        pygit2.GIT_STATUS_CONFLICTED: 'conflicted',
        pygit2.GIT_STATUS_CURRENT: 'current',
        pygit2.GIT_STATUS_IGNORED: 'ignored',
        pygit2.GIT_STATUS_INDEX_DELETED: 'index deleted',
        pygit2.GIT_STATUS_INDEX_MODIFIED: 'index modified',
        pygit2.GIT_STATUS_INDEX_NEW: 'index new',
        pygit2.GIT_STATUS_WT_DELETED: 'working tree deleted',
        pygit2.GIT_STATUS_WT_NEW: 'working tree new',
        pygit2.GIT_STATUS_WT_MODIFIED: 'working tree modified',
    }

    def __init__(self, path: str or Path, auto_init=True):
        if isinstance(path, str):
            path = Path(path)
        self.path = path
        if self.is_init:
            self.__repo = pygit2.Repository(str(self.path.joinpath('.git').abspath()))
        elif auto_init:
            self.__repo = self.init()

    @property
    def repo(self) -> pygit2.Repository:
        return self.__repo

    @property
    def is_init(self):
        return self.path.joinpath('.git').exists()

    @property
    def status(self):
        return {k: self.repo_status_map[v] for k,v in self.repo.status().items()}

    def commit(self, author: str, author_mail: str, msg: str, add_all=False):
        sig = Signature(author, author_mail)
        author, committer = sig, sig
        index = self.repo.index
        if add_all:
            index.add_all()
            index.write()
        tree = index.write_tree()
        self.repo.create_commit(self.repo.head.name, author, committer, msg, tree, [self.repo.head.get_object().hex])

    @property
    def head(self):
        return self.repo.head

    def walk(self, oid, sort_mode=pygit2.GIT_SORT_TIME):
        return self.repo.walk(oid, sort_mode)

    def init(self):
        if self.is_init:
            raise FileExistsError('repository already initialized')
        pygit2.init_repository(str(self.path.abspath()))
        repo = pygit2.Repository(str(self.path.joinpath('.git').abspath()))
        # FIXME replace with actual metadata file
        with open(str(self.path.joinpath('file').abspath()), 'wb') as f:
            f.write(os.urandom(1024))
        sig = Signature('EASI', 'easi@easi.net')
        author = sig
        committer = sig
        index = repo.index
        index.add_all()
        index.write()
        tree = index.write_tree()
        repo.create_commit('refs/heads/master', author, committer, 'EASI: initial commit', tree, [])
        return repo

if __name__ == '__main__':
    p = Path('./git_test')
    pygit2.init_repository(str(p.abspath()))
    repo = pygit2.Repository(str(p.joinpath('.git').abspath()))
    with open(str(p.joinpath('file').abspath()), 'wb') as f:
        f.write(os.urandom(1024))
    author = Signature('username', 'mail@mail.com')
    committer = Signature('username', 'mail@mail.com')
    index = repo.index
    index.add_all()
    index.write()
    tree = index.write_tree()
    oid = repo.create_commit('refs/heads/master', author, committer, 'msg', tree, [])
    print(oid)
    index = repo.index
    print(repo.status())
    # print('empty', repo.is_empty)
    # print('path', repo.path)
    # print('workdir', repo.workdir)
