# coding=utf-8


from src.ui.skeletons.dialog_input import Ui_Dialog
from src.qt import Qt, dialog_default_flags, QDialog, qt_resources, QIcon
import webbrowser
from src.ui.base.qdialog import BaseDialog
from src.ui.base.with_balloons import WithBalloons


class _InputDialog(Ui_Dialog, QDialog, WithBalloons):

    def __init__(self, title: str, text: str = '', verify_input_func=None, help_link=None, parent=None):
        QDialog.__init__(self, parent, flags=dialog_default_flags)
        WithBalloons.__init__(self)
        self.setupUi(self)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowIcon(QIcon(qt_resources.app_ico))
        self.setWindowTitle(title)
        self.label.setText(text)
        self.help_link = help_link
        self.verify_input_func = verify_input_func
        if verify_input_func:
            self.edit.textChanged.connect(self.verify_input)
        if help_link:
            self.buttonBox.addButton(self.buttonBox.Help)
            self.btn_help = self.buttonBox.button(self.buttonBox.Help)
            self.btn_help.clicked.connect(self.show_help)
        self.btn_ok = self.buttonBox.button(self.buttonBox.Ok)
        self.btn_ok.setEnabled(False)

    def verify_input(self):
        if self.verify_input_func is None:
            self.btn_ok.setEnabled(True)
            return True
        self.remove_balloons()
        error = self.verify_input_func(self.edit.text())
        if error:
            self.show_error_balloon(error, self.edit)
            self.btn_ok.setEnabled(False)
            return False
        self.btn_ok.setEnabled(True)
        return True

    def show_help(self):
        webbrowser.open_new_tab(self.help_link)

    def exec(self):
        if super(_InputDialog, self).exec() == self.Accepted:
            return self.edit.text()
        else:
            return None


class InputDialog(BaseDialog):
    def __init__(self, title: str, text: str = '', verify_input_func=None, help_link=None, parent=None):
        BaseDialog.__init__(self, _InputDialog(title, text, verify_input_func, help_link, parent))

    @staticmethod
    def make(title: str, text: str = '', verify_input_func=None, help_link=None, parent=None):
        return InputDialog(title, text, verify_input_func, help_link, parent).qobj.exec()
