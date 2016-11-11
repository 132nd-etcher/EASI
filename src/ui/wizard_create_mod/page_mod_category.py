# coding=utf-8

from src.low import help_links
from src.low.custom_logging import make_logger
from src.meta_repo.local_meta_repo import LocalMetaRepo
from src.qt import QLabel, QLineEdit, QRegExp, QRegExpValidator, QComboBox, pyqtProperty
from src.mod.mod_category import ModCategories
from .page_base import BasePage

logger = make_logger(__name__)


class ModCategoryPage(BasePage):
    @property
    def help_link(self):
        return help_links.mod_creation_category

    def __init__(self, parent=None):
        BasePage.__init__(self, parent)
        self.setTitle('Mod category')
        self.combo = QComboBox()
        self.combo.addItems([x for x in ModCategories.category_names()])
        self.registerField('category_name', self.combo, 'currentText', self.combo.currentIndexChanged)
        self.v_layout.addWidget(self.combo)