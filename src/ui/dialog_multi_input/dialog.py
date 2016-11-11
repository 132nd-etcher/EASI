# coding=utf-8

from src.qt import QDialog, Qt, QLineEdit, QLabel, QDialogButtonBox
from src.ui.skeletons.input_dialog import Ui_Dialog


# noinspection PyPep8Naming
class InputDialog(Ui_Dialog, QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent, flags=Qt.WindowSystemMenuHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        self.setWindowModality(Qt.ApplicationModal)
        self.setupUi(self)
        self.questions = {}
        self.first = None

    @property
    def btn_ok(self):
        return self.buttonBox.button(QDialogButtonBox.Ok)

    @property
    def btn_cancel(self):
        return self.buttonBox.button(QDialogButtonBox.Cancel)

    def set_title(self, title: str):
        self.setWindowTitle(title)

    def set_text(self, text: str):
        self.label.setText(text.replace('\n', '<br>'))

    def add_question(self, label, default=''):
        line = QLineEdit()
        line.setText(default)
        self.questions[label] = line
        if self.first is None:
            self.first = self.questions[label]
        self.formLayout.addRow(QLabel(label), line)

    def set_btn_ok_text(self, text: str):
        self.btn_ok.setText(text)

    def set_btn_cancel_text(self, text: str):
        self.btn_cancel.setText(text)

    def show(self):
        self.adjustSize()
        super(InputDialog, self).show()
        self.setFocus()
        self.first.setFocus()

    def showEvent(self, event):
        super(InputDialog, self).showEvent(event)
        self.first.setFocus()

    @property
    def result(self):
        return {k: self.questions[k].text() for k in self.questions}
