# coding=utf-8

from src.abstract.ui.base_dialog import AbstractBaseDialog
from src.qt import QDialog, Qt
from src.ui.skeletons.msg_dialog import Ui_Dialog


class _MsgDialog(Ui_Dialog, QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent, flags=Qt.WindowSystemMenuHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        Ui_Dialog.__init__(self)
        self.setupUi(self)


class MsgDialog(AbstractBaseDialog):
    def __init__(self, parent=None):
        AbstractBaseDialog.__init__(self, _MsgDialog(parent))

    # noinspection PyMethodOverriding
    @staticmethod
    def make(text, title=' ', parent=None):
        text = text.replace('\n', '<br>')
        dialog = MsgDialog(parent)
        qobj = dialog.qobj
        qobj.label.setText(text)
        qobj.setWindowTitle(title)
        dialog.adjust_size()
        qobj.exec()
