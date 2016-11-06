# coding=utf-8
from src.keyring.gh import GHCredentials
from src.qt import QLabel
from src.sig import SIG_CREDENTIALS_GH_AUTH_STATUS
from src.ui.base.with_balloons import WithBalloons


class GithubSetting(WithBalloons):
    def __init__(self, dialog, default_btn):
        WithBalloons.__init__(self)
        self.dialog = dialog
        self.flow = None
        self.default_btn = default_btn
        self.auth_btn.clicked.connect(self.authenticate)

        # noinspection PyUnusedLocal
        def update_auth_status(sender, text, color):
            self.status_label.setText(text)
            self.status_label.setStyleSheet('QLabel {{ color : {}; }}'.format(color))
            self.status_label.repaint()

        SIG_CREDENTIALS_GH_AUTH_STATUS.connect(update_auth_status, weak=False)

    @property
    def qt_object(self):
        return self.dialog.githubUsernameLineEdit

    @property
    def value_name(self) -> str:
        return 'gh_token'

    def show(self):
        self.dialog.githubPasswordLineEdit.setText('')
        self.dialog.githubUsernameLineEdit.setText('')

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
            self.show_error_balloon('Missing username', self.dialog.githubUsernameLineEdit)
        elif not pwd:
            self.show_error_balloon('Missing password', self.dialog.githubPasswordLineEdit)
        else:
            GHCredentials.authenticate(usr, pwd)
            self.default_btn.setDefault(True)

    @property
    def status_label(self) -> QLabel:
        return self.dialog.label_gh_status
