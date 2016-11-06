# coding=utf-8

from base64 import b64encode

from src.qt import QDialog, dialog_default_flags, Qt
from src.cfg.cfg import Config
from src.ui.base.qdialog import BaseDialog
from src.ui.skeletons.dialog_warn import Ui_Dialog


class _WarningDialog(QDialog, Ui_Dialog):
    def __init__(self, text, _id, buttons=None, title=None, parent=None):
        QDialog.__init__(self, parent, flags=dialog_default_flags)
        self.setupUi(self)
        self.id = _id
        if title is None:
            title = 'Warning'
        self.setWindowTitle(title)
        self.label.setText(text)
        self.setWindowModality(Qt.ApplicationModal)
        if buttons is None:
            buttons = 'ok'
        if buttons == 'ok':
            self.buttonBox.addButton(self.buttonBox.Ok)
            self.buttonBox.button(self.buttonBox.Ok).clicked.connect(self.accept)
        elif buttons == 'yesno':
            self.buttonBox.addButton(self.buttonBox.Yes)
            self.buttonBox.addButton(self.buttonBox.No)
            self.buttonBox.button(self.buttonBox.Yes).clicked.connect(self.accept)
            self.buttonBox.button(self.buttonBox.No).clicked.connect(self.reject)
        else:
            raise ValueError('unknown buttons value: {}'.format(buttons))

    def accept(self):
        if self.checkBox.isChecked():
            ack = set(Config().ack)
            ack.add(self.id)
            Config().ack = ack
        super(_WarningDialog, self).accept()


class WarningDialog(BaseDialog):

    buttons = dict(ok='ok', yesno='yesno')

    def __init__(self, _id: str, text: str, title: str = None, buttons: str = None, parent=None):
        BaseDialog.__init__(self, _WarningDialog(text, _id, buttons=buttons, title=title, parent=parent))

    @staticmethod
    def make(_id: str, text: str, title: str = None, buttons: str = None, parent=None):
        dialog = WarningDialog(_id, text, title, buttons, parent)
        if _id in Config().ack:
            return True
        else:
            return dialog.qobj.exec() == dialog.qobj.Accepted
