# coding=utf-8

import abc

from src.ui.skeletons.config_dialog import Ui_Settings


class AbstractSetting(metaclass=abc.ABCMeta):
    def __init__(self, dialog: Ui_Settings):
        self.dialog = dialog
        self.receiver = None
        self.tool_tip = None

    @property
    @abc.abstractproperty
    def value_name(self) -> str:
        """"""

    def show(self):
        pass

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
