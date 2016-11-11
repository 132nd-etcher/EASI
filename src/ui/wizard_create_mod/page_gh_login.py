# coding=utf-8

from src.qt import QWizardPage, QWizard, QLabel, QSpacerItem, QSizePolicy
from src.rem.gh.gh_session import GHSession
from src.ui.skeletons.form_gh_login import Ui_Form
from src.sig import SIG_CREDENTIALS_GH_AUTH_STATUS
from src.keyring.gh import GHCredentials
from src.ui.base.with_balloons import WithBalloons

class GHLoginPage(QWizardPage, Ui_Form, WithBalloons):

    def __init__(self, parent=None):
        QWizardPage.__init__(self, parent)
        WithBalloons.__init__(self)
        if GHSession().user:
            print('next')
            parent.next()
        else:
            assert isinstance(parent, QWizard)
            self.setupUi(self)
            self.intro = QLabel('In order to create a mod, you need a valid Github account.\n\n')
            self.intro.setWordWrap(True)
            self.verticalLayout_10.insertWidget(0, self.intro)
            self.verticalLayout_10.insertSpacing(1, 40)
            self.flow = None
            self.default_btn = parent.button(QWizard.NextButton)
            self.btn_gh_create.clicked.connect(self.authenticate)

            # noinspection PyUnusedLocal
            def update_auth_status(sender, text, color):
                self.label_gh_status.setText(text)
                self.label_gh_status.setStyleSheet('QLabel {{ color : {}; }}'.format(color))
                self.label_gh_status.repaint()

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

