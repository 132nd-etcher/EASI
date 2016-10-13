# coding=utf-8

from .utils import ContainedTestCase
from src.git.wrapper import Repository
from src.low.custom_path import Path

class TestGitWrapper(ContainedTestCase):

    def setUp(self):
        super(TestGitWrapper, self).setUp()
        t = self.create_temp_dir()
        self.repo = Repository(t, auto_init=True)

    def test_git_init(self):
        t = self.create_temp_dir()
        repo = Repository(t)
        with self.assertRaises(FileExistsError):
            repo.init()
        c = Path(repo.path).joinpath('.git/CONFIG')
        self.assertSequenceEqual(c.text(), ('[core]\n'
                                            '\tbare = false\n'
                                            '\trepositoryformatversion = 0\n'
                                            '\tfilemode = false\n'
                                            '\tsymlinks = false\n'
                                            '\tignorecase = true\n'
                                            '\tlogallrefupdates = true\n'))
        self.assertSequenceEqual(repo.repo.head.name, 'refs/heads/master')

    def test_repo_status(self):
        f = self.create_temp_file(create_in_dir=self.repo.path)
        self.assertDictEqual(self.repo.status,
                             {f.name: 'working tree new'})
        self.repo.commit('author', 'mail', 'message', add_all=True)
        self.assertDictEqual(self.repo.status,
                             {})
        commit_log = []
        for commit in self.repo.walk(self.repo.head.target):
            commit_log.append(commit)
        self.assertEqual(len(commit_log), 2)
        self.assertSequenceEqual(commit_log[1].message, 'EASI: initial commit')
        self.assertSequenceEqual(commit_log[0].message, 'message')
        self.assertSequenceEqual(commit_log[0].author.name, 'author')
        self.assertSequenceEqual(commit_log[0].author.email, 'mail')
        self.assertSequenceEqual(commit_log[0].committer.name, 'author')
        self.assertSequenceEqual(commit_log[0].committer.email, 'mail')
        self.assertSequenceEqual(commit_log[0].message, 'message')


