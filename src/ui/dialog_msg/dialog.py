# coding=utf-8

from src.abstract.ui.connected_dialog import AbstractConnectedDialog
from src.qt import QDialog, Qt
from src.sig import sig_msgbox
from src.ui.skeletons.msg_dialog import Ui_Dialog


class _MsgDialog(Ui_Dialog, QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent, flags=Qt.WindowSystemMenuHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        Ui_Dialog.__init__(self)
        self.setupUi(self)


class MsgDialog(AbstractConnectedDialog):
    def __init__(self, parent, main_ui_obj_name):
        AbstractConnectedDialog.__init__(self, sig_msgbox, main_ui_obj_name, _MsgDialog(parent))

    # noinspection PyMethodOverriding
    def show(self, title: str, text: str):
        text = text.replace('\n', '<br>')
        self.qobj.setWindowTitle(title)
        self.qobj.label.setText(text)
        super(MsgDialog, self).show()

    # noinspection PyMethodOverriding
    @staticmethod
    def make(text: str, title: str = ' ', parent=None):
        dialog = _MsgDialog(parent)
        dialog.label.setText(text.replace('\n', '<br>'))
        dialog.setWindowTitle(title)
        dialog.exec()
