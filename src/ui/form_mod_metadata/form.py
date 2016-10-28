# coding=utf-8

from src.qt import QWidget, Qt
from src.ui.skeletons.form_mod_metadata import Ui_Form


class FormModMetadata(Ui_Form, QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent, flags=Qt.Widget)
        self.setupUi(self)
