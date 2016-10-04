# coding=utf-8

import requests

from src.low import constants
from src.low.custom_logging import make_logger
from src.low.singleton import Singleton
from src.rem.gh.gh_objects import GHAllReleases, GHLatestRelease, GHUser, GHRepoList, GHRepo, GHAuthorization

try:
    from vault.secret import Secret
except ImportError:
    from vault.empty_secret import Secret

logger = make_logger(__name__)


# TODO: https://github.com/github/choosealicense.com/tree/gh-pages/_licenses
# TODO https://developer.github.com/v3/licenses/


class GHAnonymousSession(requests.Session, metaclass=Singleton):
    def __init__(self):
        requests.Session.__init__(self)
        self.base = ['https://api.github.com']
        self.resp = None
        self.req = None

    def build_req(self, *args):
        self.req = '/'.join(self.base + list(args))
        return self.req

    def __parse_resp(self) -> requests.models.Response:
        if self.resp is None or not self.resp.ok:
            raise ConnectionError('request failed: {} - Reason: {}'.format(self.req, self.resp.reason))
        logger.debug(self.resp.reason)
        return self.resp

    def _get(self, **kwargs) -> requests.models.Response:
        logger.debug(self.req)
        self.resp = super(GHAnonymousSession, self).get(self.req, **kwargs)
        return self.__parse_resp()

    def _put(self, **kwargs) -> requests.models.Response:
        logger.debug(self.req)
        self.resp = super(GHAnonymousSession, self).put(self.req, **kwargs)
        return self.__parse_resp()

    def _get_json(self, **kwargs) -> requests.models.Response:
        req = self._get(**kwargs)
        return req.json()

    def _post(self, data=None, json: dict = None, **kwargs) -> requests.models.Response:
        logger.debug(self.req)
        self.resp = super(GHAnonymousSession, self).post(self.req, data, json, **kwargs)
        return self.__parse_resp()

    def _patch(self, data=None, **kwargs) -> requests.models.Response:
        logger.debug(self.req)
        self.resp = super(GHAnonymousSession, self).patch(self.req, data, **kwargs)
        return self.__parse_resp()

    def _delete(self, **kwargs) -> requests.models.Response:
        logger.debug(self.req)
        self.resp = super(GHAnonymousSession, self).delete(self.req, **kwargs)
        return self.__parse_resp()

    def get_latest_release(self, user: str, repo: str) -> GHLatestRelease:
        self.build_req('repos', user, repo, 'releases', 'latest')
        return GHLatestRelease(self._get_json())

    def get_all_releases(self, user: str, repo: str):
        self.build_req('repos', user, repo, 'releases')
        return GHAllReleases(self._get_json())

    def list_user_repos(self, user: str):
        self.build_req('users', user, 'repos')
        return GHRepoList(self._get_json())

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
        json = self._get_json(auth=(username, password))
        print(json['link'])
        return [GHAuthorization(x) for x in json]

    def remove_authorization(self, username, password, auth_id):
        self.build_req('authorizations', str(auth_id))
        self._delete(auth=(username, password))

    def create_new_authorization(self, username, password) -> GHAuthorization:
        if Secret.gh_client_id is not None:
            for x in self.list_authorizations(username, password):
                assert isinstance(x, GHAuthorization)
                print(x.app().name)
                if x.app().name == constants.APP_SHORT_NAME:
                    logger.debug('removing previous authorzation')
                    self.remove_authorization(username, password, x.id)
            self.build_req('authorizations', 'clients', Secret.gh_client_id)
            json = dict(
                client_secret=Secret.gh_client_secret,
                scopes=['user', 'repo', 'delete_repo'],
                note=constants.APP_SHORT_NAME,
                note_url=constants.APP_WEBSITE
            )
            return GHAuthorization(self._put(json=json, auth=(username, password)).json())


class GHAuthenticatedSession(GHAnonymousSession, metaclass=Singleton):
    def __init__(self, token):
        GHAnonymousSession.__init__(self)
        self.headers.update(
            {
                'Authorization': 'token {}'.format(token)
            }
        )
        self.build_req('user')
        self.user = GHUser(self._get_json())

    @property
    def rate_limit(self):
        self.build_req('rate_limit')
        req = self._get()
        return req.json().get('resources', {}).get('core', {}).get('limit', 0)

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
                  name: str,
                  new_name: str = None,
                  description: str = None,
                  homepage: str = None,
                  auto_init: bool = False,
                  # license_template: str = None  # TODO GH licenses
                  ):
        if new_name is None:
            new_name = name
        self.build_req('repos', self.user.login, name)
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

    def get_repo(self, repo_name: str):
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
        if description: json['body'] = description
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
        if target_url: json['target_url'] = target_url
        if description: json['description'] = description
        if context: json['context'] = context
        print(json)
        self._post(json=json)


gh_anon = GHAnonymousSession()
gh = None

if __name__ == '__main__':
    # t = gh_anon.list_authorizations('132nd-etcher', 'kribOO5579')
    # for x in t:
    #     assert isinstance(x, GHAuthorization)
    #     print(x.app().name)
    #
    # exit(0)

    auth = gh_anon.create_new_authorization('132nd-etcher', 'kribOO5579')
    # print(auth.header)
    # print(auth.hashed_token)

    gh = GHAuthenticatedSession(auth.token)
    print(gh.user.login)
    print(gh.rate_limit)
