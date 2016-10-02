# coding=utf-8
from src.keyring.keyring import keyring
from src.low.custom_logging import make_logger
from src.rem.gh import gh_request_token, TokenRequestError
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
            token = gh_request_token(usr, pwd)
        except TokenRequestError as e:
            self.dialog.label_gh_status.setText(e.msg)
            self.dialog.label_gh_status.setStyleSheet('QLabel {{ color : red; }}')
        else:
            if token:
                keyring.gh_token = token
            self.dialog.buttonBox.button(self.dialog.buttonBox.Ok).setDefault(True)
            self.gh_token_status_changed()

    def gh_token_status_changed(self):
        self.dialog.label_gh_status.setText(keyring.gh_status_text)
        self.dialog.label_gh_status.setStyleSheet('QLabel {{ color : {}; }}'.format(keyring.gh_status_text_color))
