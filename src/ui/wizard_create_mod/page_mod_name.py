# coding=utf-8

from src.low import help_links
from src.low.custom_logging import make_logger
from src.repo.local_meta_repo import LocalMetaRepo
from src.qt import QLabel, QLineEdit, QRegExp, QRegExpValidator
from .page_base import BasePage

logger = make_logger(__name__)


class ModNamePage(BasePage):
    @property
    def help_link(self):
        return help_links.mod_creation_name

    def __init__(self, parent=None):
        BasePage.__init__(self, parent)
        self.setTitle('Mod name')
        self.label = QLabel('Choose a name for your mod')
        self.label.setWordWrap(True)
        self.edit = QLineEdit()
        self.edit.setValidator(
            QRegExpValidator(QRegExp('.*[a-zA-Z]{4,}.*'), self.edit)
        )
        self.registerField('mod_name*', self.edit)
        self.label_expl = QLabel()
        self.label_expl.setWordWrap(True)
        self.build_layout()
        # noinspection PyUnresolvedReferences
        self.edit.textChanged.connect(self.completeChanged.emit)

    # noinspection PyArgumentList
    def build_layout(self):
        self.v_layout.addWidget(self.label)
        self.v_layout.addWidget(self.edit)
        self.v_layout.addWidget(self.label_expl)

    def initializePage(self):
        super(ModNamePage, self).initializePage()
        self.label_expl.setText('The name of your mod needs to contain at least 4 contiguous letters.\n\n'
                                'It also has to be unique in the current repository ({})'
                                .format(self.field('meta_repo_name')))

    def isComplete(self):
        self.remove_balloons()
        if self.edit.hasAcceptableInput():
            meta_repo = LocalMetaRepo()[self.field('meta_repo_name')]
            if not meta_repo.mod_name_is_available_new(self.edit.text()):
                self.show_error_balloon(
                    'There is already a mod named "{}" in repository "{}"'.format(self.edit.text(),
                                                                                  meta_repo.name
                                                                                  ),
                    self.edit)
                return False
        return super(ModNamePage, self).isComplete()
