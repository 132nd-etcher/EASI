# coding=utf-8

from src.qt import *
from src.ui.skeletons.confirm_dialog import Ui_Dialog


class ConfirmDialog(Ui_Dialog, QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent, flags=Qt.WindowSystemMenuHint | Qt.WindowTitleHint)
        Ui_Dialog.__init__(self)
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    @staticmethod
    def make(question, title='Please confirm', parent=None):
        question = question.replace('\n', '<br>')
        dialog = ConfirmDialog(parent)
        dialog.label.setText(question)
        dialog.setWindowTitle(title)
        dialog.adjustSize()
        return dialog.exec() == 1
