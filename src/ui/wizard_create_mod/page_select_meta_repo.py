# coding=utf-8

from .page_base import BasePage
from src.low import help_links
from src.low.custom_logging import make_logger
from src.meta_repo.local_meta_repo import LocalMetaRepo
from src.qt import QComboBox, Qt, QLabel
from src.easi.ops import warn

logger = make_logger(__name__)


class SelectMetaRepoPage(BasePage):
    @property
    def help_link(self):
        return help_links.mod_creation_meta_repo

    def __init__(self, parent=None, default_meta_repo=None):
        BasePage.__init__(self, parent)
        self.setTitle('Metadata repository')
        self.label = QLabel('Select which repository you want to use to serve your mod to the clients.')
        self.combo = QComboBox()
        self.label_perm = QLabel()
        self.registerField('meta_repo_name', self.combo, 'currentText', self.combo.currentIndexChanged)
        self.default_meta_repo = default_meta_repo
        self.build_layout()

    # noinspection PyArgumentList
    def build_layout(self):
        self.v_layout.addWidget(self.label)
        self.v_layout.addWidget(self.combo)
        self.v_layout.addWidget(self.label_perm)

    def selection_changed(self):
        if not self.selected_meta_repo.push_perm:
            if not warn(
                    'nopushperm',
                    'You are about to create a mod in a repository in which you do not have push permission.\n\n'
                    ''
                    'Your changes will instead be sent as a "Pull Request" (an update proposal) '
                    'the the repository owner ("{}")\n\n'
                    ''
                    'Make sure you understand the implications before going further.\n\n'
                    ''
                    'Do you want to continue?'.format(
                        self.selected_meta_repo.owner
                    ),
                    buttons='yesno'
            ):
                self.combo.setCurrentIndex(0)
            else:
                self.label_perm.setText('Push permission: no')
                self.label_perm.setStyleSheet('QLabel { color : red; }')
        else:
            self.label_perm.setText('Push permission: yes')
            self.label_perm.setStyleSheet('QLabel { color : green; }')

    @property
    def selected_meta_repo(self):
        return LocalMetaRepo()[self.combo.currentText()]

    def initializePage(self):
        super(SelectMetaRepoPage, self).initializePage()
        logger.debug('prompting for meta repo')
        try:
            # noinspection PyUnresolvedReferences
            self.combo.currentIndexChanged.disconnect()
        except TypeError:
            pass
        choices = [
            LocalMetaRepo().own_meta_repo.name,
            LocalMetaRepo().root_meta_repo.name,
        ]
        for meta_repo_name in LocalMetaRepo().names:
            if meta_repo_name not in choices:
                choices.append(meta_repo_name)
        self.combo.addItems(choices)
        if self.default_meta_repo is not None:
            self.combo.setCurrentIndex(self.combo.findText(self.default_meta_repo, flags=Qt.MatchExactly))
        # noinspection PyUnresolvedReferences
        self.combo.currentIndexChanged.connect(self.selection_changed)
        self.selection_changed()
        # noinspection PyUnresolvedReferences
        self.completeChanged.emit()

    def cleanupPage(self):
        try:
            # noinspection PyUnresolvedReferences
            self.combo.currentIndexChanged.disconnect()
        except TypeError:
            pass
