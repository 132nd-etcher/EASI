# coding=utf-8

import abc
import inspect
import sys


class BaseModCategory(metaclass=abc.ABCMeta):
    @property
    def category_name(self) -> str:
        return self.__class__.__name__

    @property
    @abc.abstractproperty
    def sort_weight(self):
        """Heavier first"""


class GenericMod(BaseModCategory):
    @property
    def sort_weight(self):
        return -1


class Skin(BaseModCategory):
    @property
    def sort_weight(self):
        return 0


class Textures(BaseModCategory):
    @property
    def sort_weight(self):
        return 0


class Ui(BaseModCategory):
    @property
    def sort_weight(self):
        return 0


class Script(BaseModCategory):
    @property
    def sort_weight(self):
        return 0


class ModCategories:
    @staticmethod
    def __iter__():
        for cls_name, cls in inspect.getmembers(sys.modules[__name__], inspect.isclass):
            if cls_name != ModCategories.__name__ and not inspect.isabstract(cls):
                yield cls

    @staticmethod
    def category_names():
        return [c().category_name for w in sorted(set([x().sort_weight for x in ModCategories.__iter__()])) for c in
                sorted([x for x in ModCategories.__iter__() if x().sort_weight == w], key=lambda x: x().category_name)]
