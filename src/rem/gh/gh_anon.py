# coding=utf-8
import requests

from src.low import constants
from src.low.singleton import Singleton
from src.rem.gh.gh_errors import GithubAPIError, RateLimitationError, AuthenticationError, GHSessionError, \
    RequestFailedError
from src.rem.gh.gh_objects.gh_asset import GHAllAssets, GHAsset
from src.rem.gh.gh_objects.gh_authorization import GHAuthorization
from src.rem.gh.gh_objects.gh_release import GHRelease, GHAllReleases
from src.rem.gh.gh_objects.gh_repo import GHRepoList, GHRepo
from src.rem.gh.gh_objects.gh_user import GHUser
from src.low.custom_logging import make_logger

try:
    from vault.secret import Secret
except ImportError:
    from vault.empty_secret import Secret


logger = make_logger(__name__)


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