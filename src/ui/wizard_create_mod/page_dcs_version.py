# coding=utf-8

import semver

from src.dcs.dcs_installs import DCSInstalls, DCSInstall
from src.mod.dcs_version import DCS_VERSION_REGEX, DCSVersion

from src.low import help_links
from src.low.custom_logging import make_logger
from src.qt import QLabel, QLineEdit, QRegExp, QRegExpValidator, QToolButton, Qt, QSize, QAction, QMenu
from .page_base import BasePage

logger = make_logger(__name__)


class DCSVersionPage(BasePage):
    @property
    def help_link(self):
        return help_links.mod_creation_dcs_version

    def __init__(self, parent=None):
        BasePage.__init__(self, parent)
        self.setTitle('Initial version')
        self.label = QLabel('Specify the initial version of your mod')
        self.label.setWordWrap(True)
        self.edit = QLineEdit()
        self.edit.setValidator(
            QRegExpValidator(
                QRegExp(DCS_VERSION_REGEX), self.edit)
        )
        self.registerField('dcs_version*', self.edit)
        self.btn_pull = QToolButton()
        self.btn_pull.setMinimumSize(QSize(80, 0))
        self.btn_pull.setPopupMode(QToolButton.InstantPopup)
        self.btn_pull.setToolButtonStyle(Qt.ToolButtonTextOnly)
        self.btn_pull.setAutoRaise(False)
        self.btn_pull.setText('Pull from...')

        pull_dcs = {
            'menu': QMenu(self),
            'stable': (
                QAction('Stable', self),
                DCSInstalls().stable,
                lambda: self.__pull_dcs_version(DCSInstalls().stable)
            ),
            'beta': (
                QAction('Open Beta', self),
                DCSInstalls().beta,
                lambda: self.__pull_dcs_version(DCSInstalls().beta)
            ),
            'alpha': (
                QAction('Open Alpha', self),
                DCSInstalls().alpha,
                lambda: self.__pull_dcs_version(DCSInstalls().alpha)
            ),
        }

        for branch in ['stable', 'beta', 'alpha']:
            dcs_install = pull_dcs[branch][1]
            if dcs_install.install_path is None:
                continue
            pull_dcs['menu'].addAction(pull_dcs[branch][0])
            pull_dcs[branch][0].triggered.connect(pull_dcs[branch][2])
        self.btn_pull.setMenu(pull_dcs['menu'])

        self.label_expl = QLabel()
        self.label_expl.setWordWrap(True)

        self.v_layout.addWidget(self.label)
        self.v_layout.addWidget(self.edit)
        self.v_layout.addWidget(self.btn_pull)
        self.v_layout.addWidget(self.label_expl)

    def __pull_dcs_version(self, branch: DCSInstall):
        self.edit.setText(branch.version)

    def initializePage(self):
        super(DCSVersionPage, self).initializePage()
        self.edit.setText('')
        self.label_expl.setText('The DCS version is used to specify (in)compatibility between your mod '
                                'and specific versions of DCS.\n\n'
                                '"*" means "any"\n'
                                'a "+" at the end means "this version and all newer"')
        self.edit.textChanged.connect(self.completeChanged.emit)

    def cleanupPage(self):
        self.edit.textChanged.disconnect()
        super(DCSVersionPage, self).cleanupPage()

    def isComplete(self):
        self.remove_balloons()
        if self.edit.text() and not DCSVersion.is_valid(self.edit.text()):
            self.show_error_balloon('Invalid DCS version string', self.edit)
            return False
        return super(DCSVersionPage, self).isComplete()
