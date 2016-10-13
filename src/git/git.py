# coding=utf-8

import os

import pygit2
from pygit2 import Signature

from src.low.custom_path import Path

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
