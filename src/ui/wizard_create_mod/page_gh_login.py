# coding=utf-8

from src.qt import QWizard, QLabel, QWidget, Qt
from src.ui.skeletons.form_gh_login import Ui_Form
from src.sig import SIG_CREDENTIALS_GH_AUTH_STATUS
from src.keyring.gh import GHCredentials
from .page_base import BasePage
from src.ui.base.with_balloons import WithBalloons


class _GHLoginWidget(QWidget, Ui_Form, WithBalloons):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent, flags=Qt.Widget)
        WithBalloons.__init__(self)
        self.setupUi(self)
        self.btn_gh_create.clicked.connect(self.authenticate)
        self.default_btn = parent.parent().button(QWizard.NextButton)

        # noinspection PyUnusedLocal
        def update_auth_status(sender, text, color):
            try:
                self.label_gh_status.setText(text)
                self.label_gh_status.setStyleSheet('QLabel {{ color : {}; }}'.format(color))
                self.label_gh_status.repaint()
            except RuntimeError:
                pass

        SIG_CREDENTIALS_GH_AUTH_STATUS.connect(update_auth_status, weak=False)
        self.githubUsernameLineEdit.textChanged.connect(self.text_changed)
        self.githubPasswordLineEdit.textChanged.connect(self.text_changed)

    def text_changed(self):
        self.remove_balloons()
        self.btn_gh_create.setDefault(True)

    def authenticate(self):
        usr = self.githubUsernameLineEdit.text()
        pwd = self.githubPasswordLineEdit.text()
        if not usr:
            self.show_error_balloon('Missing username', self.githubUsernameLineEdit)
        elif not pwd:
            self.show_error_balloon('Missing password', self.githubPasswordLineEdit)
        else:
            GHCredentials.authenticate(usr, pwd)
            self.default_btn.setDefault(True)


class GHLoginPage(BasePage):
    @property
    def help_link(self):
        return None  # FIXME

    def __init__(self, parent=None):
        BasePage.__init__(self, parent)
        assert isinstance(parent, QWizard)
        self.setTitle('Login with your Github account')
        self.gh_widget = _GHLoginWidget(self)
        self.intro = QLabel('In order to create a mod, you need a valid Github account.\n\n')
        self.intro.setWordWrap(True)
        self.v_layout.addWidget(self.intro)
        self.v_layout.addSpacing(40)
        self.v_layout.addWidget(self.gh_widget)
        self.flow = None
