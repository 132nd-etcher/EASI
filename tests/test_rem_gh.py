# coding=utf-8

import time
from unittest import TestCase, mock, skipUnless

from hypothesis import strategies as st

from src.low.singleton import Singleton
from src.rem.gh import GHAnonymousSession, GHSession
from src.rem.gh.gh_objects import GHRepo, GHRepoList, GHRelease

try:
    # noinspection PyUnresolvedReferences
    from tests.unittest_secret import Secret

    token = Secret.gh_test_token
except ImportError:
    token = False


# noinspection PyPep8Naming
class TestGHAnonymousSession(TestCase):
    def __init__(self, methodName):
        TestCase.__init__(self, methodName)
        self.s = GHAnonymousSession()

    def test_users_repos(self):
        repos = self.s.list_user_repos('132nd-etcher')
        self.assertIsInstance(repos, GHRepoList)
        self.assertTrue('unittests' in repos)
        self.assertFalse('some_repo' in repos)
        repo = repos['unittests']
        self.assertIsInstance(repo, GHRepo)

    def test_user(self):
        usr = self.s.get_user('132nd-etcher')
        self.assertSequenceEqual(
            usr.get_all(),
            {
                ('url', 'https://api.github.com/users/132nd-etcher'),
                ('login', '132nd-etcher'),
                ('html_url', 'https://github.com/132nd-etcher'),
                ('id', 21277151)
            }
        )

    def test_latest_release(self):
        latest = self.s.get_latest_release('132nd-etcher', 'unittests')
        self.assertIsInstance(latest, GHRelease)
        self.assertSequenceEqual(latest.author().login, '132nd-etcher')
        self.assertFalse(latest.prerelease)
        self.assertSequenceEqual(latest.name, 'Final-release 1')
        self.assertSequenceEqual(latest.tag_name, '0.0.1.0')
        self.assertTrue('README.rst' in latest.assets())


# noinspection PyPep8Naming
@skipUnless(token, 'no test token available')
class TestGHSession(TestCase):
    def __init__(self, methodName):
        TestCase.__init__(self, methodName)
        self.s = GHSession(token)

    def setUp(self):
        self.assertGreater(self.s.rate_limit, 3000)

    def test_singleton(self):
        self.s = GHSession()
        self.assertIs(self.s, GHSession())

    @mock.patch('src.sig.sig_gh_token_status_changed.not_connected')
    def test_init_empty(self, m):
        Singleton._instances = {}
        session = GHSession()
        self.assertFalse(session is self.s)
        m.assert_called_with()

    @mock.patch('src.sig.sig_gh_token_status_changed.connected')
    def test_init_correct_token(self, m):
        Singleton._instances = {}
        session = GHSession(token)
        self.assertFalse(session is self.s)
        m.assert_called_with(Secret.gh_test_token_login)

    @mock.patch('src.sig.sig_gh_token_status_changed.wrong_token')
    def test_init_wrong_token(self, m):
        Singleton._instances = {}
        session = GHSession(st.text(min_size=1))
        self.assertFalse(session is self.s)
        m.assert_called_with()

    def test_create_repo(self):
        name = 'test_repo'
        desc = 'some description'
        self.s.create_repo(name=name, description=desc, auto_init=False)
        time.sleep(2)
        repo = self.s.get_repo(name)
        c = [
            (repo.name, name),
            (repo.default_branch, 'master'),
            (repo.archive_url, 'https://api.github.com/repos/{}/{}/{{archive_format}}{{/ref}}'.format(
                Secret.gh_test_token_login, name)),
            (repo.branches_url, 'https://api.github.com/repos/{}/{}/branches{{/branch}}'.format(
                Secret.gh_test_token_login, name)),
            (repo.clone_url, 'https://github.com/{}/{}.git'.format(
                Secret.gh_test_token_login, name)),
            (repo.commits_url, 'https://api.github.com/repos/{}/{}/commits{{/sha}}'.format(
                Secret.gh_test_token_login, name)),
            (repo.description, desc)
        ]
        for x, y in c:
            self.assertSequenceEqual(x, y)
        self.s.delete_repo(name='test_repo')
