# coding=utf-8

from abc import abstractmethod
from src.qt import QPushButton


class IWithDynamicButtons:
    @abstractmethod
    def btns_add_button(self, btn_text, btn_action, start_enabled):
        pass

    @abstractmethod
    def btns_disconnect_all(self):
        pass

    @abstractmethod
    def btns_set_enabled(self, value):
        pass

    @abstractmethod
    def btns_insert_space(self, spacer_size: int):
        pass

    @abstractmethod
    def btns_get(self, btn_name) -> QPushButton:
        pass

    @abstractmethod
    def btns_fill(self):
        pass
