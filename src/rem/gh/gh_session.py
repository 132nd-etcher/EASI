# coding=utf-8

from blinker_herald import emit, SENDER_CLASS_NAME

from src.low.custom_logging import make_logger
from src.low.singleton import Singleton
from src.rem.gh.gh_anon import GHAnonymousSession
from src.rem.gh.gh_errors import GHSessionError
from .gh_objects.gh_mail import GHMail, GHMailList
from .gh_objects.gh_repo import GHRepoList, GHRepo
from .gh_objects.gh_user import GHUser

try:
    from vault.secret import Secret
except ImportError:
    from vault.empty_secret import Secret

logger = make_logger(__name__)


# TODO: https://github.com/github/choosealicense.com/tree/gh-pages/_licenses
# TODO https://developer.github.com/v3/licenses/


class GHSession(GHAnonymousSession, metaclass=Singleton):
    session_status = dict(
        not_connected=0,
        connected=1,
        wrong_token=-1,
    )

    def __init__(self, token=None):
        GHAnonymousSession.__init__(self)
        self.user = None
        self.authenticate(token)

    @emit(only='post', sender=SENDER_CLASS_NAME)
    def authenticate(self, token):
        if token is None:
            return None
        self.headers.update(
            {
                'Authorization': 'token {}'.format(token)
            }
        )
        self.build_req('user')
        try:
            self.user = GHUser(self._get_json())
        except GHSessionError:
            return False
        return self.user.login

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
        return self._patch(json=json)

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
