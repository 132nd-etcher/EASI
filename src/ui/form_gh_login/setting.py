# coding=utf-8
from blinker_herald import signals
from src.qt import QLabel
from src.rem.gh.gh_session import GHSession
from src.rem.gh.gh_anon import GHAnonymousSession
from src.rem.gh.gh_errors import GHSessionError
from src.ui.dialog_config.settings.abstract_credential import AbstractCredentialSetting


class GithubSetting(AbstractCredentialSetting):
    def __init__(self, dialog, default_btn):
        AbstractCredentialSetting.__init__(self, dialog)
        self.flow = None
        self.default_btn = default_btn

        @signals.post_authenticate.connect_via('GHSession', weak=False)
        def status_changed(_, **kwargs):
            self.status_changed(kwargs['result'])

    @property
    def qt_object(self):
        return self.dialog.githubUsernameLineEdit

    @property
    def value_name(self) -> str:
        return 'gh_token'

    def show(self):
        self.dialog.githubPasswordLineEdit.setText('')
        self.dialog.githubUsernameLineEdit.setText('')

    def status_changed(self, result):
        super(GithubSetting, self).status_changed(result)

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
            return
        if not pwd:
            self.show_error_balloon('Missing password', self.dialog.githubPasswordLineEdit)
            return
        self.del_from_meta()
        delattr(self.store_object, 'gh_username')
        delattr(self.store_object, 'gh_password')
        self.status_label.setText('Authenticating ...')
        self.status_label.setStyleSheet('QLabel {{ color : black; }}')
        self.status_label.repaint()
        while not self.status_label.text() == 'Authenticating ...':
            pass
        try:
            auth = GHAnonymousSession().create_new_authorization(usr, pwd)
            token = auth.token
        except GHSessionError as e:
            if '401:' in e.msg:
                self.status_label.setText('Wrong username / password')
                self.status_label.setStyleSheet('QLabel {{ color : red; }}')
            else:
                self.status_label.setText(e.msg)
                self.status_label.setStyleSheet('QLabel {{ color : red; }}')
        else:
            if token:
                GHSession().authenticate(token)
                self.save_to_meta(token)
                setattr(self.store_object, 'gh_username', self.dialog.githubUsernameLineEdit.text())
                setattr(self.store_object, 'gh_password', self.dialog.githubPasswordLineEdit.text())
            self.default_btn.setDefault(True)

    @property
    def status_label(self) -> QLabel:
        return self.dialog.label_gh_status
