# coding=utf-8
import abc


# from src.ui.main_ui.interface.wrapper import interfaced_method


# # DEPRECATED candidate
# class SplashInterface:
#     @classmethod
#     @interfaced_method('splash')
#     def splash_show(cls):
#         """pass"""
#
#     @classmethod
#     @interfaced_method('splash')
#     def splash_kill(cls):
#         """pass"""
#
#     @classmethod
#     @interfaced_method('splash')
#     def splash_set_progress(cls, value: int):
#         """pass"""
#
#     @classmethod
#     @interfaced_method('splash')
#     def splash_set_text(cls, value: str):
#         """pass"""
#
#     @classmethod
#     @interfaced_method('splash')
#     def splash_add_to_progress(cls, value: int):
#         """pass"""


class AbstractSplash(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get(self):
        """"""

    @abc.abstractmethod
    def get_progress(self):
        """"""

    @abc.abstractmethod
    def current_progress(self):
        """"""

    @abc.abstractmethod
    def add_to_progress(self, value: int):
        """"""

    @abc.abstractmethod
    def show(self):
        """"""

    @abc.abstractmethod
    def kill(self):
        """"""

    @abc.abstractmethod
    def set_progress(self, value: int):
        """"""

    @abc.abstractmethod
    def set_text(self, value: str):
        """"""
