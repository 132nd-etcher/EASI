# coding=utf-8
"""Manages credentials"""

import github3
from github3.github import GitHub as GH
from github3.users import User as GHUser

from src.low import constants
from src.low.custom_logging import make_logger
from src.low.meta import Meta
from src.low.singleton import Singleton
from src.sig import sig_main_ui_states, gh_token_status_changed_sig
from .values import KeyringValues

logger = make_logger(__name__)


class Keyring(Meta, KeyringValues, metaclass=Singleton):
    """
    Manages known credentials
    """

    def __init__(self):
        Meta.__init__(self, path=constants.PATH_KEYRING_FILE)
        KeyringValues.__init__(self)
        self.__gh = None
        self.__gh_user = None
        self.__gh_status_text = 'not connected'
        self.__gh_status_text_color = 'black'

    def __setitem__(self, key, value, _write=True):
        """Immediately writes any change to file"""
        super(Keyring, self).__setitem__(key, value)
        if key == 'gh_token':
            self.validate_gh_token()
        if _write:
            self.write()

    @property
    def gh(self) -> GH:
        return self.__gh

    @property
    def gh_status_text(self):
        return self.__gh_status_text

    @property
    def gh_status_text_color(self):
        return self.__gh_status_text_color

    @property
    def gh_user(self) -> GHUser:
        return self.__gh_user

    @property
    def gh_username(self):
        if self.gh_user:
            return self.gh_user.name

    def validate_gh_token(self):
        if self.gh_token:
            try:
                assert isinstance(self.gh_token, str)
                self.__gh = github3.login(token=self.gh_token)
                self.__gh_user = self.gh.user()
                # self.__gh_status = '<font color="green">connected as {}</font>'.format(self.gh_username)
                self.__gh_status_text = 'connected as {}'.format(self.gh_username)
                self.__gh_status_text_color = 'green'
            except github3.GitHubError:
                # self.__gh_status = '<font color="red">invalid token, please create a new one</font>'
                self.__gh_status_text = 'invalid token, please create a new one'
                self.__gh_status_text_color = 'red'
        else:
            self.__gh_status_text = 'not connected'
            self.__gh_status_text_color = 'black'
        gh_token_status_changed_sig.send()

    def validate_tokens(self):
        self.validate_gh_token()


def init_keyring():
    logger.info('keyring: validating tokens')
    sig_main_ui_states.keyring_validation_start()
    keyring.validate_tokens()
    logger.info('keyring: tokens validated')
    sig_main_ui_states.keyring_validation_finished()


logger.info('keyring: initializing')
keyring = Keyring()
logger.info('keyring: initialized')
