# coding=utf-8

from dropbox import Dropbox as BaseDropbox, DropboxOAuth2FlowNoRedirect
from dropbox.exceptions import AuthError
import webbrowser
try:
    from vault.secret import Secret
except ImportError:
    from vault.empty_secret import Secret
from src.low import constants
from src.__version__ import version
from src.low.singleton import Singleton
from src.low.custom_logging import make_logger
from src.sig import db_token_status_changed_sig

logger = make_logger(__name__)

class DBSession(metaclass=Singleton):
    session_status = dict(
        not_connected=0,
        connected=1,
        wrong_token=-1,
    )

    def __init__(self, token=None):
        self.abbrev_version = '.'.join([str(x) for x in (version.major, version.minor, version.revision)])
        self.agent = '{}/{}'.format(constants.APP_SHORT_NAME, self.abbrev_version)
        self.session = None
        self.account = None
        if token is None:
            db_token_status_changed_sig.not_connected()
        else:
            self.authenticate(token)

    def authenticate(self, token):
        try:
            self.session = BaseDropbox(token)
            self.account = self.session.users_get_current_account()
            db_token_status_changed_sig.connected(self.account.name.given_name)
        except AuthError:
            logger.error('wrong token')
            db_token_status_changed_sig.wrong_token()

    @staticmethod
    def start_auth_flow():
        flow = DropboxOAuth2FlowNoRedirect(Secret.db_app_key, Secret.db_app_secret)
        webbrowser.open(flow.start(), autoraise=True)
        return flow

    @staticmethod
    def finish_auth_flow(flow, code):
        token, user_id = flow.finish(code)
        return token
