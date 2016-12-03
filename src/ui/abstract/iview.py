# coding=utf-8
from abc import abstractmethod


class IView:
    @abstractmethod
    def build_model(self):
        """Populates the model using self.add_row"""
        pass

    @abstractmethod
    def reset_model(self):
        pass

    @abstractmethod
    def on_show(self, *args, **kwargs):
        pass

    @abstractmethod
    def on_hide(self, *args, **kwargs):
        pass
