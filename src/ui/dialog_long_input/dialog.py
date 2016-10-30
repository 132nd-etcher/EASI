# coding=utf-8

from src.ui.skeletons.dialog_long_input import Ui_Dialog
from src.ui.base.qdialog import BaseDialog
from src.qt import QDialog, dialog_default_flags, QIcon, qt_resources


class _LongInputDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent, flags=dialog_default_flags)
        self.setupUi(self)
        self.btn_ok = self.buttonBox.button(self.buttonBox.Ok)
        self.btn_cancel = self.buttonBox.button(self.buttonBox.Cancel)
        self.btn_ok.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)
        self.setWindowIcon(QIcon(qt_resources.app_ico))


class LongInputDialog(BaseDialog):
    def __init__(self, parent=None):
        BaseDialog.__init__(self, _LongInputDialog(parent))

    @property
    def qobj(self) -> _LongInputDialog:
        return super(LongInputDialog, self).qobj

    def show(self, title, label_text: str = None, init_text=''):
        self.qobj.setWindowTitle(title)
        if label_text is None:
            self.qobj.label.hide()
        else:
            self.qobj.label.setText(label_text)
        self.qobj.textBrowser.setText(init_text)
        self.qobj.show()

    @staticmethod
    def make(parent=None, title: str = None, label_text: str = None, init_text=''):
        dialog = LongInputDialog(parent)
        if title:
            dialog.qobj.setWindowTitle(title)
        if label_text is None:
            dialog.qobj.label.hide()
        else:
            dialog.qobj.label.setText(label_text)
        dialog.qobj.textBrowser.setText(init_text)
        dialog.qobj.show()
        if not dialog.qobj.exec() == dialog.qobj.Accepted:
            return None
        else:
            return dialog.qobj.textBrowser.toPlainText()
