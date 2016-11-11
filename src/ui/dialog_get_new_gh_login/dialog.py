# coding=utf-8

from src.qt import QDialog, dialog_default_flags, qt_resources, QIcon
from src.rem.gh.gh_session import GHSession
from src.ui.base.qdialog import BaseDialog
from src.ui.form_gh_login.form import GHLoginForm
from src.ui.skeletons.dialog_gh_login import Ui_Dialog


class _GetNewGHLoginDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent=parent, flags=dialog_default_flags)
        self.setupUi(self)
        self.btn_exit.clicked.connect(self.close)
        self.setWindowTitle('Github login')
        self.setWindowIcon(QIcon(qt_resources.app_ico))
        layout = self.layout()
        self.form = GHLoginForm(self, self.btn_exit)
        layout.insertWidget(0, self.form)
        self.form.githubUsernameLineEdit.setFocus()

    def setup(self):
        self.form.setup()

    def close(self):
        super(_GetNewGHLoginDialog, self).close()

    def show(self):
        self.form.show()
        super(_GetNewGHLoginDialog, self).show()

    def exec(self):
        super(_GetNewGHLoginDialog, self).exec()
        return GHSession().has_valid_token


class GetNewGHLoginDialog(BaseDialog):
    def __init__(self, parent=None):
        BaseDialog.__init__(self, _GetNewGHLoginDialog(parent))
        self.qobj.setup()
        self.qobj.show()

    @staticmethod
    def make(parent=None) -> bool:
        """Returns True if a valid GH account was added"""
        dialog = GetNewGHLoginDialog(parent)
        dialog.qobj.setup()
        return dialog.qobj.exec()
