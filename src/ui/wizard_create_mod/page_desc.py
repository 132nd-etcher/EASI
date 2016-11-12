# coding=utf-8

from src.low import help_links
from src.low.custom_logging import make_logger
from src.qt import QLabel, QTextEdit
from .page_base import BasePage

logger = make_logger(__name__)


class DescriptionPage(BasePage):
    @property
    def help_link(self):
        return help_links.mod_creation_desc

    def __init__(self, parent=None):
        BasePage.__init__(self, parent)
        self.setTitle('Description')
        self.label = QLabel('(optional)\n\n'
                            'Describe your mod:')
        self.label.setWordWrap(True)
        self.edit = QTextEdit()
        self.registerField('mod_desc', self.edit, 'plainText')
        self.build_layout()

    # noinspection PyArgumentList
    def build_layout(self):
        self.v_layout.addWidget(self.label)
        self.v_layout.addWidget(self.edit)

    def initializePage(self):
        super(DescriptionPage, self).initializePage()
        self.edit.setText('')
