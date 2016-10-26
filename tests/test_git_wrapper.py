# coding=utf-8

import pytest
import os
from src.git.wrapper import Repository
from src.low.custom_path import Path


class TestGitWrapper:
    def test_git_init(self, tmpdir):
        t = str(tmpdir)
        repo = Repository(t)
        with pytest.raises(FileExistsError):
            repo.init()
        c = Path(repo.path).joinpath('.git/CONFIG')
        # noinspection SpellCheckingInspection
        assert c.text() == ('[core]\n'
                            '\tbare = false\n'
                            '\trepositoryformatversion = 0\n'
                            '\tfilemode = false\n'
                            '\tsymlinks = false\n'
                            '\tignorecase = true\n'
                            '\tlogallrefupdates = true\n')
        assert repo.repo.head.name == 'refs/heads/master'

    def test_repo_status(self, tmpdir):
        repo = Repository(str(tmpdir))
        f = str(tmpdir.join('f'))
        with open(f, 'w') as _f:
            _f.write('')
        assert repo.status == {os.path.basename(f): 'working tree new'}
        repo.commit('author', 'mail', 'message', add_all=True)
        assert repo.status == {}
        commit_log = []
        for commit in repo.walk(repo.head.target):
            commit_log.append(commit)
        assert len(commit_log) == 2
        assert commit_log[1].message == 'EASI: initial commit'
        assert commit_log[0].message == 'message'
        assert commit_log[0].author.name == 'author'
        assert commit_log[0].author.email == 'mail'
        assert commit_log[0].committer.name == 'author'
        assert commit_log[0].committer.email == 'mail'
        assert commit_log[0].message == 'message'
