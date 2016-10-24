# coding=utf-8

import os
import time
from json import loads, dumps
from unittest import TestCase, mock, skipUnless, skipIf

import pytest
import requests
from blinker_herald import signals
from httmock import response, urlmatch, with_httmock
from hypothesis import strategies as st

from src.low.custom_path import Path
from src.low.singleton import Singleton
from src.rem.gh.gh_objects.gh_release import GHAllAssets
from src.rem.gh.gh_objects.gh_release import GHRelease
from src.rem.gh.gh_objects.gh_repo import GHRepo, GHRepoList
from src.rem.gh.gh_objects.gh_user import GHUser
from src.rem.gh.gh_session import GHAnonymousSession, GHSession, GithubAPIError, RateLimitationError, GHSessionError, \
    RequestFailedError

try:
    # noinspection PyUnresolvedReferences
    from vault.secret import Secret

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
PATCH = 'patch'


class GHResource:
    def __init__(self, path):
        self.path = path

    def get(self):
        return Path(self.path).text()

    def patch(self, request):
        req_j = request.body.decode()
        req_d = loads(req_j)
        local_j = Path(self.path).text()
        local_d = loads(local_j)
        assert isinstance(local_d, dict)
        local_d.update(req_d)
        local_j = dumps(local_d)
        return response(200, local_j, HEADERS, 'OK', 5, request)


current_user = 'octocat'


def check_fail(url, request):
    if url.path.endswith('le_resp_is_empty'):
        return None
    if url.path.endswith('le_api_is_down'):
        return response(500, None, HEADERS, 'Error', 5, request)
    if url.path.endswith('le_rate_is_exceeded'):
        return response(403, {'message': 'API rate limit exceeded for '}, HEADERS, 'Error', 5, request)
    if url.path.endswith('le_random_error'):
        return response(402, {'message': 'Random message'}, HEADERS, 'Error', 5, request)
    return 'ok'


def get_file_path(url):
    if '/user/' in url.path:
        file_path = url.netloc + url.path.replace('/user/', '/user/{}/'.format(current_user)) + '.json'
    else:
        file_path = url.netloc + url.path + '.json'
    if not os.path.exists(file_path):
        file_path = 'tests/{}'.format(file_path)
    return file_path


@urlmatch(netloc=ENDPOINT)
def mock_gh_api(url, request):
    assert isinstance(request, requests.models.PreparedRequest)
    fail = check_fail(url, request)
    if not fail == 'ok':
        return fail
    file_path = get_file_path(url)
    try:
        if request.method == 'GET':
            content = GHResource(file_path).get()
        elif request.method == 'PATCH':
            content = GHResource(file_path).patch(request)
        else:
            raise ValueError('request not handled: {}'.format(request.method))
    except EnvironmentError:
        return response(404, {}, HEADERS, 'FileNotFound: {}'.format(file_path), 5, request)
    return response(200, content, HEADERS, 'Success', 5, request)


@with_httmock(mock_gh_api)
def test_api_down():
    with pytest.raises(GithubAPIError):
        GHAnonymousSession().get_user('le_api_is_down')


@with_httmock(mock_gh_api)
def test_rate_exceeded():
    with pytest.raises(RateLimitationError):
        GHAnonymousSession().get_user('le_rate_is_exceeded')


@with_httmock(mock_gh_api)
def test_other_error():
    with pytest.raises(GHSessionError):
        GHAnonymousSession().get_user('le_random_error')


@with_httmock(mock_gh_api)
def test_request_failed():
    with pytest.raises(RequestFailedError):
        GHAnonymousSession().get_user('le_resp_is_empty')


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
def test_primary_email():
    global current_user
    current_user = 'octocat'
    mail = GHSession().primary_email
    assert mail.email == 'octocat@github.com'
    current_user = 'octodog'
    mail = GHSession().primary_email
    assert mail is None
    current_user = 'octocub'
    mail = GHSession().primary_email
    assert mail is None
    current_user = 'octocat'


@with_httmock(mock_gh_api)
def test_get_repos():
    global current_user
    current_user = 'octocat'
    repos = GHSession().list_own_repos()
    assert len(repos) == 1
    r = repos['Hello-World']
    assert r.name == 'Hello-World'
    assert r.full_name == 'octocat/Hello-World'


@with_httmock(mock_gh_api)
def test_edit_repo():
    s = GHSession()
    s.user = mock.MagicMock(login='octocat')
    repo = s.get_repo('ze_repo')
    assert repo.name == 'Hello-World'
    resp = GHSession().edit_repo('octocat', 'ze_repo', new_name='ze_other_repo')
    assert isinstance(resp, requests.models.Response)
    assert resp.status_code == 200
    repo = s.get_repo('ze_repo')
    d = loads(resp.content.content.decode())
    for k in d.keys():
        if k == 'name':
            assert d[k] == 'ze_other_repo'
        else:
            try:
                x = getattr(repo, k)
                if callable(x):
                    continue
                assert d[k] == x
            except AttributeError:
                pass


@with_httmock(mock_gh_api)
def test_list_own_repos():
    s = GHSession()
    s.user = mock.MagicMock(login='octocat')
    repos = s.list_own_repos()
    assert len(repos) == 1
    assert 'Hello-World' in repos


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
        try:
            repos = self.s.list_user_repos('easitest')
        except RateLimitationError:
            return
        self.assertIsInstance(repos, GHRepoList)
        self.assertTrue('unittests' in repos)
        self.assertFalse('some_repo' in repos)
        repo = repos['unittests']
        self.assertIsInstance(repo, GHRepo)

    def test_latest_release(self):
        try:
            latest = self.s.get_latest_release('132nd-etcher', 'unittests')
        except RateLimitationError:
            return
        self.assertIsInstance(latest, GHRelease)
        self.assertSequenceEqual(latest.author().login, '132nd-etcher')
        self.assertFalse(latest.prerelease)
        self.assertSequenceEqual(latest.name, 'Final-release 1')
        self.assertSequenceEqual(latest.tag_name, '0.0.1.0')
        self.assertTrue('README.rst' in latest.assets())


@pytest.mark.usefixtures('config')
class TestGHSessionAuthentication:
    s = None

    @pytest.fixture(autouse=True)
    def new_gh_session(self, qtbot):
        result = -1

        @signals.post_authenticate.connect_via('GHSession', weak=False)
        def check_result(_, **kwargs):
            nonlocal result
            result = kwargs['result']

        Singleton.wipe_instances('GHSession')
        self.s = GHSession()
        qtbot.wait_until(lambda: result is None)

    def test_init_wrong_token(self, qtbot):
        result = -1

        @signals.post_authenticate.connect_via('GHSession', weak=False)
        def check_result(_, **kwargs):
            nonlocal result
            result = kwargs['result']

        self.s.authenticate(st.text(min_size=1))
        qtbot.wait_until(lambda: result is False)

    @skipUnless(token, 'no test token available')
    def test_init_correct_token(self, qtbot):
        result = -1

        @signals.post_authenticate.connect_via('GHSession', weak=False)
        def check_result(_, **kwargs):
            nonlocal result
            result = kwargs['result']

        self.s.authenticate(token)
        qtbot.wait_until(lambda: result == Secret.gh_test_login)


@skipUnless(token, 'no test token available')
@pytest.mark.usefixtures('config')
class TestGHSession:
    s = None

    @pytest.fixture(autouse=True)
    def gh_session(self, qtbot):
        result = -1

        @signals.post_authenticate.connect_via('GHSession', weak=False)
        def check_result(_, **kwargs):
            nonlocal result
            result = kwargs['result']

        if token:
            Singleton.wipe_instances('GHSession')
            self.s = GHSession(token)
            qtbot.wait_until(lambda: result == Secret.gh_test_login)

    @skipUnless(token, 'no test token available')
    def test_primary_email(self):
        assert Secret.gh_test_usermail == self.s.primary_email.email

    @skipUnless(token, 'no test token available')
    @skipUnless(os.getenv('DOLONGTESTS', False) is not False, 'skipping long tests')
    def test_create_repo(self):
        # noinspection PyBroadException
        try:
            self.s.delete_repo(name='test_repo')
        except:
            pass
        name = 'test_repo'
        desc = 'some description'
        self.s.create_repo(name=name, description=desc, auto_init=False)
        time.sleep(2)
        repo = self.s.get_repo(name)
        c = [
            (repo.name, name),
            (repo.default_branch, 'master'),
            (repo.archive_url, 'https://api.github.com/repos/{}/{}/{{archive_format}}{{/ref}}'.format(
                Secret.gh_test_login, name)),
            (repo.branches_url, 'https://api.github.com/repos/{}/{}/branches{{/branch}}'.format(
                Secret.gh_test_login, name)),
            (repo.clone_url, 'https://github.com/{}/{}.git'.format(
                Secret.gh_test_login, name)),
            (repo.commits_url, 'https://api.github.com/repos/{}/{}/commits{{/sha}}'.format(
                Secret.gh_test_login, name)),
            (repo.description, desc)
        ]
        for x, y in c:
            assert x == y
        self.s.delete_repo(name='test_repo')


def test_user(gh_anon):
    try:
        usr = gh_anon.get_user('132nd-etcher')
    except RateLimitationError:
        return
    assert isinstance(usr, GHUser)
    assert usr.id == 21277151
    assert usr.type == 'User'
