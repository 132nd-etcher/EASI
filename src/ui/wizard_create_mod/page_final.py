# coding=utf-8

from src.qt import QWizardPage, QLabel, QVBoxLayout


class FinalPage(QWizardPage):

    def __init__(self, parent=None):
        QWizardPage.__init__(self, parent)
        self.setLayout(QVBoxLayout(self))
        self.label = QLabel('Your mod is ready to be created !\n\n'
                            'Click "Finish" to begin adding files to it.')
        self.layout().addWidget(self.label)