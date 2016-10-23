# coding=utf-8

from src.qt import QDialog, Qt
from src.ui.base.qdialog import BaseDialog
from src.ui.skeletons.msg_dialog import Ui_Dialog
from .interface import MsgboxInterface
from src.abstract.msg_interface import MsgInterface


class _MsgDialog(Ui_Dialog, QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent, flags=Qt.WindowSystemMenuHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        Ui_Dialog.__init__(self)
        self.setupUi(self)


class MsgDialog(BaseDialog, MsgInterface):
    def __init__(self, parent):
        BaseDialog.__init__(self, _MsgDialog(parent))

    @property
    def qobj(self) -> _MsgDialog:
        return super(MsgDialog, self).qobj

    # noinspection PyMethodOverriding
    def show(self, title: str, text: str):
        text = text.replace('\n', '<br>')
        self.qobj.setWindowTitle(title)
        self.qobj.label.setText(text)
        self.adjust_size()
        self.qobj.show()
