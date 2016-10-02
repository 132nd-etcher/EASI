# coding=utf-8

from src.abstract.ui.base_dialog import AbstractBaseDialog
from src.qt import *
from src.ui.skeletons.input_dialog import Ui_Dialog


class _Input_dialog(Ui_Dialog, QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent, flags=Qt.WindowSystemMenuHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        self.setupUi(self)


class InputDialog(AbstractBaseDialog):
    def __init__(self, parent=None):
        AbstractBaseDialog.__init__(self, _Input_dialog(parent))

    # noinspection PyMethodOverriding
    @staticmethod
    def make(text, title=' ', inputs: list = None,
             ok_btn_text: str = None, cancel_btn_txt: str = None,
             parent=None):
        if inputs is None:
            inputs = []
        output = {}
        text = text.replace('\n', '<br>')
        base = InputDialog(parent)
        dialog = base.qobj
        assert isinstance(inputs, list)
        for label, default in inputs:
            output[label] = QLineEdit(default)
            dialog.formLayout.addRow(QLabel(label), output[label])
        if ok_btn_text is not None:
            dialog.buttonBox.button(QDialogButtonBox.Ok).setText(ok_btn_text)
        if cancel_btn_txt is not None:
            dialog.buttonBox.button(QDialogButtonBox.Cancel).setText(cancel_btn_txt)
        dialog.label.setText(text)
        dialog.setWindowTitle(title)
        base.adjust_size()
        if dialog.exec() == 1:
            output = {k: output[k].text() for k in output}
            return output
        else:
            return None
