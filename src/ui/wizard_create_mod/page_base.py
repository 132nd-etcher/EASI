# coding=utf-8

import abc

from src.qt import QWizardPage, QVBoxLayout
from src.ui.base.with_balloons import WithBalloons


class BasePage(QWizardPage, WithBalloons):
    def __init__(self, parent=None):
        QWizardPage.__init__(self, parent)
        WithBalloons.__init__(self)
        self.setLayout(QVBoxLayout(self))
        self.setTitle(' ')
        self.setSubTitle(' ')

    @property
    def v_layout(self) -> QVBoxLayout:
        return self.layout()

    @abc.abstractproperty
    def help_link(self):
        """"""