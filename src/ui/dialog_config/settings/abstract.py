# coding=utf-8

import abc

from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QToolTip

from src.ui.skeletons.config_dialog import Ui_Settings


class AbstractSetting(metaclass=abc.ABCMeta):
    def __init__(self, dialog: Ui_Settings, value_name):
        self.dialog = dialog
        self.receiver = None
        self.tool_tip = None
        self.value_name = value_name

    @abc.abstractmethod
    def show(self):
        """"""

    @property
    @abc.abstractproperty
    def store_class(self):
        """"""

    @property
    @abc.abstractproperty
    def store_object(self):
        """"""

    @abc.abstractmethod
    def setup(self):
        """"""
