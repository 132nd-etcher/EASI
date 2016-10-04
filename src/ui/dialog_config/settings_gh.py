# coding=utf-8
from src.keyring.keyring import keyring
from src.low.custom_logging import make_logger
from src.rem.gh import GHSessionError, GHAnonymousSession, GHSession
from src.sig import SignalReceiver, gh_token_status_changed_sig
from src.ui.dialog_config.abstract_config_dialog_child import AbstractConfigDialogChild
from src.ui.skeletons.config_dialog import Ui_Settings

logger = make_logger(__name__)


class GHSettings(AbstractConfigDialogChild):
    def save_settings(self):
        return True

    def load_settings(self):
        pass

    def __init__(self, dialog: Ui_Settings):
        self.dialog = dialog
        self.dialog.btn_gh_create.clicked.connect(self.gh_create_token)
        self.receiver = SignalReceiver(self)
        self.receiver[gh_token_status_changed_sig] = self.gh_token_status_changed

    def setup(self):
        self.dialog.githubUsernameLineEdit.textChanged.connect(self.set_default_button_to_create_gh_token)
        self.dialog.githubPasswordLineEdit.textChanged.connect(self.set_default_button_to_create_gh_token)

    def set_default_button_to_create_gh_token(self):
        self.dialog.btn_gh_create.setDefault(True)

    def gh_create_token(self):
        usr = self.dialog.githubUsernameLineEdit.text()
        pwd = self.dialog.githubPasswordLineEdit.text()
        if not usr:
            logger.error('missing username')  # TODO
            return
        if not pwd:
            logger.error('missing password')  # TODO
            return
        self.dialog.label_gh_status.setText('Authenticating ...')
        self.dialog.label_gh_status.setStyleSheet('QLabel {{ color : black; }}')
        try:
            auth = GHAnonymousSession().create_new_authorization(usr, pwd)
            token = auth.token
        except GHSessionError as e:
            self.dialog.label_gh_status.setText(e.msg)
            self.dialog.label_gh_status.setStyleSheet('QLabel {{ color : red; }}')
        else:
            if token:
                keyring.gh_token = token
                GHSession().authenticate(token)
            self.dialog.buttonBox.button(self.dialog.buttonBox.Ok).setDefault(True)

    def gh_token_status_changed(self, **kwargs):
        status = kwargs.get('status')
        if status == GHSession.session_status['not_connected']:
            self.dialog.label_gh_status.setText('Not connected')
            self.dialog.label_gh_status.setStyleSheet('QLabel { color : black; }')
        if status == GHSession.session_status['wrong_token']:
            self.dialog.label_gh_status.setText('Token not accepted; please create a new one')
            self.dialog.label_gh_status.setStyleSheet('QLabel { color : red; }')
        if status == GHSession.session_status['connected']:
            self.dialog.label_gh_status.setText('Connected as: {}'.format(kwargs.get('username')))
            self.dialog.label_gh_status.setStyleSheet('QLabel { color : green; }')
