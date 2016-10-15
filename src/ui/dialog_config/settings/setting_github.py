# coding=utf-8
from src.qt import QLabel, QToolTip, QPoint
from src.rem.gh.gh_session import GHSession, GHAnonymousSession, GHSessionError
from src.sig import sig_gh_token_status_changed, CustomSignal
from src.ui.dialog_config.settings.abstract_credential import AbstractCredentialSetting


class GithubSetting(AbstractCredentialSetting):
    @property
    def value_name(self) -> str:
        return 'gh_token'

    def show(self):
        self.dialog.githubPasswordLineEdit.setText('')
        self.dialog.githubUsernameLineEdit.setText('')

    @property
    def token_changed_signal(self) -> CustomSignal:
        return sig_gh_token_status_changed

    def __init__(self, dialog):
        AbstractCredentialSetting.__init__(self, dialog)
        self.flow = None

    def setup(self):
        self.dialog.githubUsernameLineEdit.textChanged.connect(self.text_changed)
        self.dialog.githubPasswordLineEdit.textChanged.connect(self.text_changed)

    def text_changed(self):
        self.remove_balloons()
        self.dialog.btn_gh_create.setDefault(True)

    @property
    def auth_btn(self):
        return self.dialog.btn_gh_create

    def authenticate(self):
        usr = self.dialog.githubUsernameLineEdit.text()
        pwd = self.dialog.githubPasswordLineEdit.text()
        if not usr:
            # noinspection PyArgumentList
            # QToolTip.showText(self.dialog.githubUsernameLineEdit.mapToGlobal(QPoint(0, 0)), 'missing username')
            self.show_error_balloon('Missing username', self.dialog.githubUsernameLineEdit)
            return
        if not pwd:
            # noinspection PyArgumentList
            # QToolTip.showText(self.dialog.githubPasswordLineEdit.mapToGlobal(QPoint(0, 0)), 'missing password')
            self.show_error_balloon('Missing password', self.dialog.githubPasswordLineEdit)
            return
        self.status_label.setText('Authenticating ...')
        self.status_label.setStyleSheet('QLabel {{ color : black; }}')
        try:
            auth = GHAnonymousSession().create_new_authorization(usr, pwd)
            token = auth.token
        except GHSessionError as e:
            self.status_label.setText(e.msg)
            self.status_label.setStyleSheet('QLabel {{ color : red; }}')
        else:
            if token:
                GHSession().authenticate(token)
                self.save_to_meta(token)
            self.dialog.buttonBox.button(self.dialog.buttonBox.Ok).setDefault(True)

    @property
    def session_object(self):
        return GHSession

    @property
    def status_label(self) -> QLabel:
        return self.dialog.label_gh_status
