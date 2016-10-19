# coding=utf-8

import os
import time
from unittest import TestCase, mock, skipUnless, skipIf

import pytest
from httmock import response, urlmatch, with_httmock
from hypothesis import strategies as st

from src.low.singleton import Singleton
from src.rem.gh.gh_objects.gh_release import GHAllAssets
from src.rem.gh.gh_objects.gh_release import GHRelease
from src.rem.gh.gh_objects.gh_repo import GHRepo, GHRepoList
from src.rem.gh.gh_objects.gh_user import GHUser
from src.rem.gh.gh_session import GHAnonymousSession, GHSession

try:
    # noinspection PyUnresolvedReferences
    from tests.unittest_secret import Secret

    token = Secret.gh_test_token
except ImportError:
    token = False


def test_build_req():
    s = GHAnonymousSession()
    assert s.build_req('test', 'test') == 'https://api.github.com/test/test'
    with pytest.raises(ValueError):
        s.build_req()
    with pytest.raises(TypeError):
        s.build_req(1)


ENDPOINT = r'(.*\.)?api\.github\.com$'
HEADERS = {'content-type': 'application/json'}
GET = 'get'


class GHResource:
    def __init__(self, path):
        self.path = path

    def get(self):
        with open(self.path, 'r') as f:
            content = f.read()
        return content


@urlmatch(netloc=ENDPOINT, method=GET)
def mock_gh_api(url, request):
    file_path = url.netloc + url.path + '.json'
    if not os.path.exists(file_path):
        file_path = 'tests/{}'.format(file_path)
    try:
        content = GHResource(file_path).get()
    except EnvironmentError:
        return response(404, {}, HEADERS, 'FileNotFound', 5, request)
    return response(200, content, HEADERS, 'Success', 5, request)


@with_httmock(mock_gh_api)
def test_get_repo():
    repo = GHAnonymousSession().get_repo('132nd-etcher', 'EASI')

    assert repo is not None
    assert isinstance(repo, GHRepo)
    assert repo.name == 'EASI'


@with_httmock(mock_gh_api)
def test_get_user():
    user = GHAnonymousSession().get_user('octocat')

    assert user.login == 'octocat'
    assert user.email == 'octocat@github.com'


@with_httmock(mock_gh_api)
def test_get_latest_release():
    latest = GHAnonymousSession().get_latest_release('132nd-etcher', 'EASI')
    assert latest.assets_url == 'https://api.github.com/repos/octocat/Hello-World/releases/1/assets'
    assert isinstance(latest.assets(), GHAllAssets)
    assert len(latest.assets()) == 1
    assert isinstance(latest.author(), GHUser)
    assert latest.body == 'Description of the release'
    assert latest.created_at == '2013-02-27T19:35:32Z'
    assert latest.draft is False
    assert latest.html_url == 'https://github.com/octocat/Hello-World/releases/v1.0.0'
    assert latest.name == 'v1.0.0'
    assert latest.prerelease is False
    assert latest.published_at == '2013-02-27T19:35:32Z'
    assert latest.version == 'v1.0.0'
    assert latest.url == 'https://api.github.com/repos/octocat/Hello-World/releases/1'


@with_httmock(mock_gh_api)
def test_gh_asset():
    asset = GHAnonymousSession().get_asset('132nd-etcher', 'EASI', 1, 1)
    assert asset.url == 'https://api.github.com/repos/octocat/Hello-World/releases/assets/1'
    assert asset.id == 1
    assert asset.name == 'example.zip'
    assert asset.label == 'short description'
    assert isinstance(asset.uploader(), GHUser)
    assert asset.content_type == 'application/zip'
    assert asset.state == 'uploaded'
    assert asset.size == 1024
    assert asset.download_count == 42
    assert asset.created_at == '2013-02-27T19:35:32Z'
    assert asset.updated_at == '2013-02-27T19:35:32Z'
    assert asset.browser_download_url == 'https://github.com/octocat/Hello-World/releases/download/v1.0.0/example.zip'


@with_httmock(mock_gh_api)
def test_get_all_asset():
    all_assets = GHAnonymousSession().get_all_assets('132nd-etcher', 'EASI', 1)
    assert isinstance(all_assets, GHAllAssets)
    assert len(all_assets) == 1


# noinspection PyPep8Naming
@skipIf(os.getenv('APPVEYOR'), 'AppVeyor gets 403 from GH all the time')
class TestGHAnonymousSession(TestCase):
    def __init__(self, methodName):
        TestCase.__init__(self, methodName)
        self.s = GHAnonymousSession()

    def test_users_repos(self):
        repos = self.s.list_user_repos('easitest')
        self.assertIsInstance(repos, GHRepoList)
        self.assertTrue('unittests' in repos)
        self.assertFalse('some_repo' in repos)
        repo = repos['unittests']
        self.assertIsInstance(repo, GHRepo)

    def test_user(self):
        usr = self.s.get_user('132nd-etcher')
        print(usr.get_all())
        self.assertSequenceEqual(
            usr.get_all(),
            {
                ('public_gists', 0), ('blog', None), ('bio', None), ('public_repos', 36), ('company', None),
                ('location', None), ('avatar_url', 'https://avatars.githubusercontent.com/u/21277151?v=3'),
                ('id', 21277151), ('login', '132nd-etcher'), ('html_url', 'https://github.com/132nd-etcher'),
                ('type', 'User'), ('updated_at', '2016-10-18T22:43:35Z'),
                ('repos_url', 'https://api.github.com/users/132nd-etcher/repos'),
                ('created_at', '2016-08-27T11:20:43Z'),
                ('email', None), ('url', 'https://api.github.com/users/132nd-etcher')
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
@skipIf(os.getenv('APPVEYOR'), 'AppVeyor gets 403 from GH all the time')
class TestGHSession(TestCase):
    def __init__(self, methodName):
        Singleton.wipe_instances()
        TestCase.__init__(self, methodName)
        self.s = GHSession(token)

    def setUp(self):
        self.assertGreater(self.s.rate_limit, 3000)

    def test_singleton(self):
        self.assertIs(self.s, GHSession())

    @mock.patch('src.sig.sig_gh_token_status_changed.not_connected')
    def test_init_empty(self, m):
        Singleton.wipe_instances()
        session = GHSession()
        self.assertFalse(session is self.s)
        m.assert_called_with()
        Singleton.wipe_instances()
        self.s = GHSession(token)

    @mock.patch('src.sig.sig_gh_token_status_changed.connected')
    def test_init_correct_token(self, m):
        Singleton.wipe_instances()
        session = GHSession(token)
        self.assertFalse(session is self.s)
        m.assert_called_with(Secret.gh_test_token_login)
        Singleton.wipe_instances()
        self.s = GHSession(token)

    @mock.patch('src.sig.sig_gh_token_status_changed.wrong_token')
    def test_init_wrong_token(self, m):
        Singleton.wipe_instances()
        session = GHSession(st.text(min_size=1))
        self.assertFalse(session is self.s)
        m.assert_called_with()
        Singleton.wipe_instances()
        self.s = GHSession(token)

    def test_primary_email(self):
        assert Secret.gh_usermail == self.s.primary_email.email

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
