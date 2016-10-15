# coding=utf-8

import abc
from src.cfg import config
from src.cfg.cfg import Config
from .abstract import AbstractSetting
from src.qt import QPoint, QToolTip


class AbstractConfigSetting(AbstractSetting, metaclass=abc.ABCMeta):
    def __init__(self, dialog):
        AbstractSetting.__init__(self, dialog)
        if not hasattr(self.store_class, self.value_name):
            raise NameError('{} object has no value: {}'.format(self.store_class.__class__.__name__, self.value_name))

    @property
    def store_class(self):
        return Config

    @property
    def store_object(self):
        return config

    @property
    def value_type(self):
        """Type of value as defined in meta"""
        return getattr(self.store_class, self.value_name).type

    @property
    def value_default(self):
        return getattr(self.store_class, self.value_name).default

    @property
    def value(self):
        """Current value as set in meta"""
        return getattr(self.store_object, self.value_name)

    def validation_fail(self):
        self.qt_object.setStyleSheet('border: 2px solid red;')

    def validation_success(self):
        self.qt_object.setStyleSheet('')

    @property
    def has_changed(self) -> bool:
        return self.value != self.get_value_from_dialog()

    def save_to_meta(self) -> bool:
        if self.validate_dialog_value():
            self.validation_success()
            setattr(self.store_object, self.value_name, self.get_value_from_dialog())
            return True
        else:
            self.validation_fail()

    def load_from_meta(self) -> bool:
        self.set_dialog_value(self.value)
        return True

    @abc.abstractmethod
    def validate_dialog_value(self) -> bool:
        """"""

    @abc.abstractmethod
    def get_value_from_dialog(self):
        """"""

    @abc.abstractmethod
    def set_dialog_value(self, value):
        """"""

    @abc.abstractmethod
    def dialog_has_changed_methods(self) -> list:
        """List of methods that are called when the value in the dialog has changed"""
