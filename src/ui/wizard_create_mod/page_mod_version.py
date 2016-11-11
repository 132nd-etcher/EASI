# coding=utf-8

import semver

from src.low import help_links
from src.low.custom_logging import make_logger
from src.qt import QLabel, QLineEdit, QRegExp, QRegExpValidator
from .page_base import BasePage

logger = make_logger(__name__)

SEMVER_REGEX = '(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)' \
               '(?:-[\da-z\-]+(?:\.[\da-z\-]+)*)?(?:\+[\da-z\-]' \
               '+(?:\.[\da-z\-]+)*)?'


class ModVersionPage(BasePage):
    @property
    def help_link(self):
        return help_links.mod_creation_version

    def __init__(self, parent=None):
        BasePage.__init__(self, parent)
        self.setTitle('Initial version')
        self.label = QLabel('Specify the initial version of your mod')
        self.label.setWordWrap(True)
        self.edit = QLineEdit()
        self.edit.setValidator(
            QRegExpValidator(
                QRegExp(SEMVER_REGEX), self.edit)
        )
        self.registerField('mod_version*', self.edit)
        self.label_expl = QLabel()
        self.label_expl.setWordWrap(True)
        self.v_layout.addWidget(self.label)
        self.v_layout.addWidget(self.edit)
        self.v_layout.addWidget(self.label_expl)
        self.edit.textChanged.connect(self.completeChanged.emit)
        self.completeChanged.emit()

    def initializePage(self):
        super(ModVersionPage, self).initializePage()
        self.edit.setText('0.0.1')
        self.label_expl.setText('The version must be a valid SemVer (see "Help" to learn about SemVer).\n\n'
                                'You can also let EASI manage your mod\'s versionning for you.')

    def isComplete(self):
        self.remove_balloons()
        try:
            semver.parse(self.edit.text())
        except ValueError:
            self.show_error_balloon('This is not a valid SemVer', self.edit)
            return False
        return super(ModVersionPage, self).isComplete()
