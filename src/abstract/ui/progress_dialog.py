# coding=utf-8

from src.qt import QDialog, Qt


# noinspection PyPep8Naming
class BaseProgressDialogInterface:
    def setupUi(self, dialog):
        raise NotImplementedError

    def setWindowModality(self, modality):
        raise NotImplementedError


class BaseProgressDialog(QDialog, BaseProgressDialogInterface):
    def setupUi(self, dialog):
        raise NotImplementedError

    def __init__(self, parent):
        QDialog.__init__(self, parent, Qt.WindowTitleHint)
        self.setupUi(self)
        self.setWindowModality(Qt.ApplicationModal)

    def reject(self):
        pass
