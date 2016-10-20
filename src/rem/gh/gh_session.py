# coding=utf-8

import requests

from src.low import constants
from src.low.custom_logging import make_logger
from src.low.singleton import Singleton
from src.sig import sig_gh_token_status_changed
from .gh_objects.gh_authorization import GHAuthorization
from .gh_objects.gh_release import GHAllReleases, GHRelease
from .gh_objects.gh_asset import GHAsset, GHAllAssets
from .gh_objects.gh_repo import GHRepoList, GHRepo
from .gh_objects.gh_user import GHUser
from .gh_objects.gh_mail import GHMail, GHMailList

try:
    from vault.secret import Secret
except ImportError:
    from vault.empty_secret import Secret

logger = make_logger(__name__)


class GHSessionError(Exception):
    def __init__(self, msg):
        self.msg = msg
        Exception.__init__(self, msg)


class RequestFailedError(GHSessionError):
    pass


class AuthenticationError(GHSessionError):
    pass


class RateLimitationError(GHSessionError):
    pass


class GithubAPIError(GHSessionError):
    pass


# TODO: https://github.com/github/choosealicense.com/tree/gh-pages/_licenses
# TODO https://developer.github.com/v3/licenses/


class GHAnonymousSession(requests.Session, metaclass=Singleton):
    def __init__(self):
        requests.Session.__init__(self)
        self.base = ['https://api.github.com']
        self.__resp = None
        self.req = None

    @property
    def resp(self) -> requests.models.Response:
        return self.__resp

    def build_req(self, *args):
        if not args:
            raise ValueError('request is empty')
        for x in args:
            if not isinstance(x, str):
                raise TypeError('expected a string, got: {} ({})'.format(x, args))
        self.req = '/'.join(self.base + list(args))
        return self.req

    def __parse_resp_error(self):
        logger.error(self.req)
        if self.resp.status_code >= 500:
            raise GithubAPIError(r'Github API seems to be down, check https://status.github.com/')
        else:
            code = self.resp.status_code
            reason = self.resp.reason
            msg = [str(code), reason]
            json = self.resp.json()
            if json:
                msg.append('GH_MSG: {}'.format(json.get('message')))
                msg.append('GH_DOC: {}'.format(json.get('documentation_url')))
                if code == 403 and json.get('message').startswith('API rate limit exceeded for '):
                    raise RateLimitationError(': '.join(msg))
            if code == 401:
                raise AuthenticationError(': '.join(msg))
            else:
                raise GHSessionError(': '.join(msg))

    def __parse_resp(self) -> requests.models.Response:
        if self.__resp is None:
            raise RequestFailedError('did not get any response from: {}'.format(self.req))
        if not self.__resp.ok:
            self.__parse_resp_error()
        logger.debug(self.__resp.reason)
        return self.__resp

    def _get(self, **kwargs) -> requests.models.Response:
        logger.debug(self.req)
        self.__resp = super(GHAnonymousSession, self).get(self.req, **kwargs)
        return self.__parse_resp()

    def _put(self, **kwargs) -> requests.models.Response:
        logger.debug(self.req)
        self.__resp = super(GHAnonymousSession, self).put(self.req, **kwargs)
        return self.__parse_resp()

    def _get_json(self, **kwargs) -> requests.models.Response:
        req = self._get(**kwargs)
        return req.json()

    def _post(self, data=None, json: dict = None, **kwargs) -> requests.models.Response:
        logger.debug(self.req)
        self.__resp = super(GHAnonymousSession, self).post(self.req, data, json, **kwargs)
        return self.__parse_resp()

    def _patch(self, data=None, **kwargs) -> requests.models.Response:
        logger.debug(self.req)
        self.__resp = super(GHAnonymousSession, self).patch(self.req, data, **kwargs)
        return self.__parse_resp()

    def _delete(self, **kwargs) -> requests.models.Response:
        logger.debug(self.req)
        self.__resp = super(GHAnonymousSession, self).delete(self.req, **kwargs)
        return self.__parse_resp()

    def get_latest_release(self, user: str, repo: str) -> GHRelease:
        self.build_req('repos', user, repo, 'releases', 'latest')
        return GHRelease(self._get_json())

    def get_all_releases(self, user: str, repo: str):
        self.build_req('repos', user, repo, 'releases')
        return GHAllReleases(self._get_json())

    def get_all_assets(self, user: str, repo: str, release_id: int):
        self.build_req('repos', user, repo, 'releases', str(release_id), 'assets')
        return GHAllAssets(self._get_json())

    def get_asset(self, user: str, repo: str, release_id: int, asset_id: int):
        self.build_req('repos', user, repo, 'releases', str(release_id), 'assets', str(asset_id))
        return GHAsset(self._get_json())

    def list_user_repos(self, user: str):
        self.build_req('users', user, 'repos')
        return GHRepoList(self._get_json())

    def get_repo(self, user: str, repo: str):
        self.build_req('repos', user, repo)
        return GHRepo(self._get_json())

    def get_user(self, user: str):
        self.build_req('users', user)
        return GHUser(self._get_json())

    def list_authorizations(self, username, password) -> list:

        auth_list = []

        def __add_auth(json):
            nonlocal auth_list
            for x in json:
                auth_list.append(GHAuthorization(x))

        self.build_req('authorizations')
        req = self._get(auth=(username, password))
        __add_auth(req.json())
        while 'next' in req.links:
            req = self.get(req.links['next']['url'], auth=(username, password))
            __add_auth(req.json())
        return auth_list

    def remove_authorization(self, username, password, auth_id):
        self.build_req('authorizations', str(auth_id))
        self._delete(auth=(username, password))

    def create_new_authorization(self, username, password) -> GHAuthorization:
        if Secret.gh_client_id is not None:
            for x in self.list_authorizations(username, password):
                assert isinstance(x, GHAuthorization)
                if x.app().name == constants.APP_SHORT_NAME:
                    logger.debug('removing previous authorization')
                    self.remove_authorization(username, password, x.id)
            self.build_req('authorizations', 'clients', Secret.gh_client_id)
            json = dict(
                client_secret=Secret.gh_client_secret,
                scopes=['user', 'repo', 'delete_repo'],
                note=constants.APP_SHORT_NAME,
                note_url=constants.APP_WEBSITE
            )
            return GHAuthorization(self._put(json=json, auth=(username, password)).json())


class GHSession(GHAnonymousSession, metaclass=Singleton):
    session_status = dict(
        not_connected=0,
        connected=1,
        wrong_token=-1,
    )

    def __init__(self, token=None):
        GHAnonymousSession.__init__(self)
        self.user = None
        if token:
            self.authenticate(token)
        else:
            sig_gh_token_status_changed.not_connected()

    def authenticate(self, token):
        self.headers.update(
            {
                'Authorization': 'token {}'.format(token)
            }
        )
        self.build_req('user')
        try:
            self.user = GHUser(self._get_json())
        except GHSessionError:
            sig_gh_token_status_changed.wrong_token()
        else:
            sig_gh_token_status_changed.connected(self.user.login)

    @property
    def rate_limit(self):
        self.build_req('rate_limit')
        req = self._get()
        return req.json().get('resources', {}).get('core', {}).get('remaining', 0)

    @property
    def email_addresses(self) -> GHMailList:
        self.build_req('user', 'emails')
        return GHMailList(self._get_json())

    @property
    def primary_email(self) -> GHMail or None:
        for mail in self.email_addresses:
            assert isinstance(mail, GHMail)
            if mail.primary and mail.verified:
                return mail
        return None

    def create_repo(self,
                    name: str,
                    description: str = None,
                    homepage: str = None,
                    auto_init: bool = False,
                    # license_template: str = None
                    ):
        self.build_req('user', 'repos')
        json = dict(
            name=name,
            description=description,
            homepage=homepage,
            auto_init=auto_init
        )
        self._post(json=json)

    def edit_repo(self,
                  user, repo,
                  new_name: str = None,
                  description: str = None,
                  homepage: str = None,
                  auto_init: bool = False,
                  # license_template: str = None  # TODO GH licenses
                  ):
        if new_name is None:
            new_name = repo
        self.build_req('repos', user, repo)
        json = dict(name=new_name)
        if description:
            json['body'] = description
        if homepage:
            json['homepage'] = homepage
        if auto_init:
            json['auto_init'] = auto_init
        self._patch(json=json)

    def delete_repo(self, name: str):
        self.build_req('repos', self.user.login, name)
        self._delete()

    def list_own_repos(self):
        self.build_req('user', 'repos')
        return GHRepoList(self._get_json())

    def get_repo(self, repo_name: str, **_):
        self.build_req('repos', self.user.login, repo_name)
        return GHRepo(self._get_json())

    def create_pull_request(
            self,
            title: str,
            user, repo,
            description: str = None,
            head: str = None, base: str = 'master'):
        if head is None:
            head = '{}:master'.format(self.user.login)
        json = dict(
            title=title,
            head=head,
            base=base
        )
        if description:
            json['body'] = description
        self.build_req('repos', user, repo, 'pulls')
        self._post(json=json)

    # FIXME this is just for the lulz
    def create_status(
            self,
            repo: str,
            sha: str,
            state: str,
            target_url: str = None,
            description: str = None,
            context: str = None):
        self.build_req('repos', self.user.login, repo, 'statuses', sha)
        json = dict(state=state)
        if target_url:
            json['target_url'] = target_url
        if description:
            json['description'] = description
        if context:
            json['context'] = context
        self._post(json=json)
