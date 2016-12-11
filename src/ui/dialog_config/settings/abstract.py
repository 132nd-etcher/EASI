# coding=utf-8

import abc

from src.ui.skeletons.config_dialog import Ui_Settings
from src.ui.widget_balloon.widget import WidgetBalloon


class AbstractSetting(metaclass=abc.ABCMeta):
    def __init__(self, dialog: Ui_Settings):
        self.dialog = dialog
        self.receiver = None
        self.balloons = []

    @property
    @abc.abstractproperty
    def qt_object(self):
        """"""

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

    def remove_balloons(self):
        while self.balloons:
            balloon = self.balloons.pop()
            balloon.hide()
            del balloon

    def show_error_balloon(self, text, qt_object=None):
        if qt_object is None:
            qt_object = self.qt_object
        self.balloons.append(WidgetBalloon.error(qt_object, text))
