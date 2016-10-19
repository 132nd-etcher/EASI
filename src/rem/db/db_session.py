# coding=utf-8

import webbrowser

from dropbox import Dropbox as BaseDropbox, DropboxOAuth2FlowNoRedirect
from dropbox.exceptions import AuthError

try:
    from vault.secret import Secret
except ImportError:
    from vault.empty_secret import Secret
from src.low import constants
from src.__version__ import __version__
from src.low.singleton import Singleton
from src.low.custom_logging import make_logger
from src.sig import sig_db_token_status_changed

logger = make_logger(__name__)


class DBSession(metaclass=Singleton):
    session_status = dict(
        not_connected=0,
        connected=1,
        wrong_token=-1,
    )

    def __init__(self, token=None):
        self.agent = '{}/{}'.format(constants.APP_SHORT_NAME, __version__)
        self.session = None
        self.account = None
        if token is None:
            sig_db_token_status_changed.not_connected()
        else:
            self.authenticate(token)

    def authenticate(self, token):
        try:
            self.session = BaseDropbox(token)
            self.account = self.session.users_get_current_account()
            sig_db_token_status_changed.connected(self.account.name.given_name)
        except AuthError:
            logger.error('wrong token')
            sig_db_token_status_changed.wrong_token()

    @staticmethod
    def start_auth_flow():
        flow = DropboxOAuth2FlowNoRedirect(Secret.db_app_key, Secret.db_app_secret)
        webbrowser.open(flow.start(), autoraise=True)
        return flow

    @staticmethod
    def finish_auth_flow(flow, code):
        token, _ = flow.finish(code)
        return token
