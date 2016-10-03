# coding=utf-8

from src.qt import QDialog, Qt


class BaseProgressDialog(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent, Qt.WindowTitleHint)
        self.setupUi(self)
        self.setWindowModality(Qt.ApplicationModal)

    def reject(self):
        pass
