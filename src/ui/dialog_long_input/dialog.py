# coding=utf-8

import webbrowser

from src.qt import QDialog, dialog_default_flags, QIcon, qt_resources, Qt
from src.ui.base.qdialog import BaseDialog
from src.ui.base.with_balloons import WithBalloons
from src.ui.skeletons.dialog_long_input import Ui_Dialog


class _LongInputDialog(QDialog, Ui_Dialog, WithBalloons):
    def __init__(self, title: str, text: str, default: str = '', verify_input_func=None, help_link=None, parent=None):
        QDialog.__init__(self, parent, flags=dialog_default_flags)
        WithBalloons.__init__(self)
        self.setupUi(self)
        self.btn_ok = self.buttonBox.button(self.buttonBox.Ok)
        self.btn_cancel = self.buttonBox.button(self.buttonBox.Cancel)
        self.btn_ok.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)
        self.setWindowIcon(QIcon(qt_resources.app_ico))
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowTitle(title)
        self.label.setText(text)
        self.textBrowser.setText(default)
        self.verify_input_func = verify_input_func
        if verify_input_func:
            self.textBrowser.textChanged.connect(self.validate)
            self.btn_ok.setEnabled(False)
        self.help_link = help_link
        if help_link:
            self.buttonBox.addButton(self.buttonBox.Help)
            self.btn_help = self.buttonBox.button(self.buttonBox.Help)
            self.btn_help.clicked.connect(self.show_help)

    def show_help(self):
        webbrowser.open_new_tab(self.help_link)

    def validate(self):
        self.remove_balloons()
        error = self.verify_input_func(self.textBrowser.toPlainText())
        if error:
            self.btn_ok.setEnabled(False)
            self.show_error_balloon(error, self.textBrowser)
        else:
            self.btn_ok.setEnabled(True)

    def exec(self):
        if super(_LongInputDialog, self).exec() == self.Accepted:
            return self.textBrowser.toPlainText()
        else:
            return None


class LongInputDialog(BaseDialog):
    def __init__(self, title: str, text: str, default: str = '', verify_input_func=None, help_link=None, parent=None):
        BaseDialog.__init__(self, _LongInputDialog(title, text, default, verify_input_func, help_link, parent))

    @staticmethod
    def make(title: str, text: str, default: str = '', verify_input_func=None, help_link=None, parent=None):
        return LongInputDialog(title, text, default, verify_input_func, help_link, parent).qobj.exec()
