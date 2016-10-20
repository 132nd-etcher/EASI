# coding=utf-8

from src.qt import QDialog, Qt, QLineEdit, QLabel, QDialogButtonBox
from src.ui.skeletons.input_dialog import Ui_Dialog


# noinspection PyPep8Naming
class InputDialog(Ui_Dialog, QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent, flags=Qt.WindowSystemMenuHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        self.setupUi(self)

    # noinspection PyMethodOverriding
    @staticmethod
    def make(text,
             title=' ',
             inputs: list = None,
             ok_btn_text: str = None,
             cancel_btn_txt: str = None,
             parent=None) -> dict:
        if inputs is None:
            inputs = []
        output = {}
        text = text.replace('\n', '<br>')
        dialog = InputDialog(parent)
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
        dialog.adjustSize()
        # base.adjust_size()
        if dialog.exec() == 1:
            return {k: output[k].text() for k in output}
        else:
            return {}
