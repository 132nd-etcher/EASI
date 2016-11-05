# coding=utf-8

from src.qt import QDialog, dialog_default_flags, QWidget
from src.ui.base.qdialog import BaseDialog
from src.ui.widget_git_files.widget import GitFilesWidget
from src.ui.skeletons.form_repo_details import Ui_Form
from src.meta_repo.meta_repo import MetaRepo


class _RepoDetailsDialog(QDialog, Ui_Form):
    def __init__(self, repo: MetaRepo, parent=None):
        QDialog.__init__(self, parent, flags=dialog_default_flags)
        self.setupUi(self)
        self.__repo = repo
        self.files_widget = GitFilesWidget(self.repo.local, self)
        self.main_layout.addWidget(self.files_widget)
        self.btn_local_files.setChecked(True)
        self.files_widget.setHidden(False)
        self.btn_local_files.clicked.connect(lambda: self.show_widget(self.files_widget))
        self.repo = repo

    @property
    def repo(self):
        return self.__repo

    @repo.setter
    def repo(self, value):
        self.__repo = value
        self.setWindowTitle('Showing files for: {}'.format(self.repo.path.abspath()))

    def show_widget(self, widget: QWidget):
        self.files_widget.setHidden(True)
        widget.setHidden(False)


class RepoDetailsDialog(BaseDialog):
    def __init__(self, repo: MetaRepo, parent=None):
        BaseDialog.__init__(self, _RepoDetailsDialog(repo, parent))
        self.qobj.show()
