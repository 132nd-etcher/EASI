# coding=utf-8

from dropbox import Dropbox as BaseDropbox
import webbrowser
try:
    from vault.secret import Secret
except ImportError:
    from vault.empty_secret import Secret
from src.low import constants
from src.__version__ import version
from src.keyring import keyring
from src.low.custom_logging import make_logger

logger = make_logger(__name__)

class Dropbox:

    def __init__(self):
        self.abbrev_version = '.'.join([version.major, version.minor, version.reset_revision()]
        self.agent = '{}/{}'.format(constants.APP_SHORT_NAME, self.abbrev_version)
        self.session = dropbox.Dropbox(token, usr)

def dropbox_auth():
    flow = dropbox.DropboxOAuth2FlowNoRedirect(Secret.db_app_key, Secret.db_app_secret)
    webbrowser.open(flow.start(), autoraise=True)
    code = input()
    token, user_id = flow.finish(code)
    print(token, user_id)

dropbox = Dropbox()
