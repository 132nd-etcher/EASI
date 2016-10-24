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
        self.formLayout.addRow(QLabel(label), line)

    def set_btn_ok_text(self, text: str):
        self.btn_ok.setText(text)

    def set_btn_cancel_text(self, text: str):
        self.btn_cancel.setText(text)

    def show(self):
        self.adjustSize()
        super(InputDialog, self).show()

    @property
    def result(self):
        return {k: self.questions[k].text() for k in self.questions}

    # # noinspection PyMethodOverriding
    # @staticmethod
    # def make(text,
    #          title=' ',
    #          inputs: list = None,
    #          ok_btn_text: str = None,
    #          cancel_btn_txt: str = None,
    #          parent=None) -> dict:
    #     if inputs is None:
    #         inputs = []
    #     dialog = InputDialog(parent)
    #     dialog.set_title(title)
    #     dialog.set_text(text)
    #
    #     assert isinstance(inputs, list)
    #     for x in inputs:
    #         try:
    #             label, default = x
    #         except IndexError:
    #             label, default = x, ''
    #         dialog.add_question(label, default)
    #     if ok_btn_text is not None:
    #         dialog.set_btn_ok_text(ok_btn_text)
    #     if cancel_btn_txt is not None:
    #         dialog.set_btn_cancel_text(cancel_btn_txt)
    #     if dialog.exec() == 1:
    #         return {k: dialog.questions[k].text() for k in dialog.questions}
    #     else:
    #         return {}
