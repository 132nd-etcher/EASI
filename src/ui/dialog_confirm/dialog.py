# coding=utf-8

from src.qt import QDialog, Qt
from src.ui.skeletons.confirm_dialog import Ui_Dialog


class ConfirmDialog(Ui_Dialog, QDialog):
    def __init__(self, question: str, title='Please confirm', parent=None):
        QDialog.__init__(self, parent, flags=Qt.WindowSystemMenuHint | Qt.WindowTitleHint)
        Ui_Dialog.__init__(self)
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        question = question.replace('\n', '<br>')
        self.label.setText(question)
        self.setWindowTitle(title)
        self.adjustSize()

    @staticmethod
    def make(question: str, title: str = 'Please confirm', parent=None) -> bool:
        dialog = ConfirmDialog(question, title, parent)
        return dialog.exec() == 1
