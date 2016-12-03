# coding=utf-8

from src.qt import Qt, QWidget
from src.repo.repo_local_view import LocalRepoTableView
from src.ui.base.qwidget import BaseQWidget
from src.ui.skeletons.form_repository_table import Ui_Form


class _MetaRepoTable(Ui_Form, QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent, flags=Qt.Widget)
        self.setupUi(self)
        self.model = LocalRepoTableView(self.table, parent=self, btns_layout=self.verticalLayout)


class MetaRepoTable(BaseQWidget):
    def __init__(self, parent=None):
        BaseQWidget.__init__(self, _MetaRepoTable(parent))
