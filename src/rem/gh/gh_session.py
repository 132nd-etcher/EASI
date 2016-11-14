# coding=utf-8

from blinker_herald import emit, SENDER_CLASS_NAME
from blinker import signal
from src.sig import SIG_CREDENTIALS_GH_AUTH_STATUS, SigProgress

from src.low.custom_logging import make_logger
from src.low.singleton import Singleton
from src.rem.gh.gh_anon import GHAnonymousSession
from src.rem.gh.gh_errors import GHSessionError
from src.keyring.keyring import Keyring
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
        self.gh_user = None
        self.user = None
        self.authenticate(token)
        if self.user is False:
            SIG_CREDENTIALS_GH_AUTH_STATUS.send(
                text='Token was invalidated; please create a new one',
                color='red'
            )
        elif self.user is None:
            SIG_CREDENTIALS_GH_AUTH_STATUS.send(text='Ready', color='black')
        else:
            SIG_CREDENTIALS_GH_AUTH_STATUS.send(text=self.user, color='green')

        # noinspection PyUnusedLocal
        def update_credentials(sender, *args, **kwargs):
            self.authenticate(Keyring().gh_token)

        signal('Keyring_gh_token_value_changed').connect(update_credentials, weak=False)

    @property
    def has_valid_token(self):
        return isinstance(self.user, str)

    @emit(only='post', sender=SENDER_CLASS_NAME)
    def authenticate(self, token):
        if token is None:
            self.user = None
        else:
            self.headers.update(
                {
                    'Authorization': 'token {}'.format(token)
                }
            )
            self.build_req('user')
            try:
                self.gh_user = GHUser(self._get_json())
                self.user = self.gh_user.login
            except GHSessionError:
                self.user = False
        return self.user

    def check_authentication(self, _raise=True):
        if not isinstance(self.user, str):
            if _raise:
                raise GHSessionError('unauthenticated')
            return False

    @property
    def own_meta_repo(self):
        if not self.user:
            return None
        try:
            return self.get_repo('EASIMETA')
        except FileNotFoundError:
            SigProgress().set_progress_text('Creating EASIMETA repository on Github for user: {}'.format(self.user))
            SigProgress().set_progress(0)
            self.create_repo(name='EASIMETA',
                             description='Meta repository for EASI mods',
                             auto_init=True)
            self.check_authentication()
            ref = self.get_ref(self.user, 'EASIMETA', 'master')
            sha = ref.object().sha
            self.create_status('EASIMETA', sha, 'success',
                               description='This commit was made by EASI',
                               context='EASI')
            SigProgress().set_progress(100)
            return self.get_repo('EASIMETA')

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
        self.check_authentication()
        self.build_req('repos', self.user, name)
        self._delete()

    def list_own_repos(self):
        self.build_req('user', 'repos')
        return GHRepoList(self._get_json())

    def get_repo(self, repo_name: str, user: str = None, **_):
        if user is None:
            self.check_authentication()
            user = self.user
        self.build_req('repos', user, repo_name)
        try:
            return GHRepo(self._get_json())
        except GHSessionError as e:
            if e.msg.startswith('404'):
                raise FileNotFoundError('repository does not exist')

    def create_pull_request(
            self,
            title: str,
            user, repo,
            description: str = None,
            head: str = None, base: str = 'master'):
        self.check_authentication()
        if head is None:
            head = '{}:master'.format(self.user)
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
        self.check_authentication()
        self.build_req('repos', self.user, repo, 'statuses', sha)
        json = dict(state=state)
        if target_url:
            json['target_url'] = target_url
        if description:
            json['description'] = description
        if context:
            json['context'] = context
        self._post(json=json)
