# coding=utf-8

from src.qt import QLabel, QVBoxLayout
from .page_base import BasePage


class FinalPage(BasePage):

    @property
    def help_link(self):
        return None

    def __init__(self, parent=None):
        BasePage.__init__(self, parent)
        self.setTitle('Almost done!')
        self.setLayout(QVBoxLayout(self))
        self.label = QLabel('Your mod is ready to be created !\n\n'
                            'Click "Finish" to begin adding files to it.')
        self.layout().addWidget(self.label)