# coding=utf-8

from src.low import constants
from src.qt import QDialog, dialog_default_flags, qt_resources, QIcon
from src.ui.base.qdialog import BaseDialog
from src.ui.form_gh_login.form import GHLoginForm
from src.ui.skeletons.dialog_gh_login import Ui_Dialog


class _GHLoginDialog(QDialog, Ui_Dialog):

    def __init__(self, parent=None):
        if parent is None:
            parent = constants.MAIN_UI
        QDialog.__init__(self, parent=parent, flags=dialog_default_flags)
        self.setupUi(self)
        self.btn_exit.clicked.connect(self.close)
        self.setWindowTitle('Github login')
        self.setWindowIcon(QIcon(qt_resources.app_ico))
        layout = self.layout()
        self.forms = {
            'github': GHLoginForm(self, self.btn_exit)
        }
        layout.insertWidget(0, self.forms['github'])

    def setup(self):
        for form in self.forms.values():
            form.setup()



class GHLoginDialog(BaseDialog):

    def __init__(self, parent=None):
        BaseDialog.__init__(self, _GHLoginDialog(parent))
        self.qobj.setup()



if __name__ == '__main__':
    from src.qt import QApplication
    import sys
    from src.keyring.keyring import Keyring
    qt_app = QApplication([])
    dialog = GHLoginDialog()
    dialog.qobj.show()
    from src.rem.gh.gh_session import GHSession
    GHSession(Keyring().gh_token)
    sys.exit(qt_app.exec())
