# coding=utf-8

import webbrowser

from src.qt import Qt, dialog_default_flags, QDialog, qt_resources, QIcon
from src.ui.base.qdialog import BaseDialog
from src.ui.skeletons.dialog_select import Ui_Dialog


class _SelectDialog(QDialog, Ui_Dialog):
    def __init__(self, choices: list, title: str, label_text: str = '', help_link=None, parent=None):
        QDialog.__init__(self, parent=parent, flags=dialog_default_flags)
        self.setupUi(self)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowIcon(QIcon(qt_resources.app_ico))
        self.setWindowTitle(title)
        self.label.setText(label_text)
        self.combo.addItems(choices)
        if help_link:
            self.help_link = help_link
            self.buttonBox.addButton(self.buttonBox.Help)
            self.btn_help = self.buttonBox.button(self.buttonBox.Help)
            self.btn_help.clicked.connect(self.show_help)

    def show_help(self):
        webbrowser.open_new_tab(self.help_link)

    def exec(self):
        if super(_SelectDialog, self).exec() == _SelectDialog.Accepted:
            return self.combo.currentText()
        else:
            return None


class SelectDialog(BaseDialog):
    def __init__(self, choices: list, title: str, label_text: str = '', help_link=None, parent=None):
        BaseDialog.__init__(self, _SelectDialog(choices, title, label_text, help_link, parent))

    @staticmethod
    def make(choices: list, title: str, label_text: str = '', help_link=None, parent=None):
        return SelectDialog(choices, title, label_text, help_link, parent).qobj.exec()
