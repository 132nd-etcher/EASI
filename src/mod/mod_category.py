# coding=utf-8

import abc
import inspect
import sys


class BaseModCategory(metaclass=abc.ABCMeta):
    @property
    @abc.abstractproperty
    def category_name(self) -> str:
        """"""

    @property
    @abc.abstractproperty
    def sorting_weight(self):
        """Heavier first"""


class GenericMod(BaseModCategory):
    @property
    def sorting_weight(self):
        return -1

    @property
    def category_name(self) -> str:
        return 'Generic mod'


class Skin(BaseModCategory):
    @property
    def sorting_weight(self):
        return 0

    @property
    def category_name(self) -> str:
        return 'Skin'


class Texture(BaseModCategory):
    @property
    def sorting_weight(self):
        return 0

    @property
    def category_name(self) -> str:
        return 'Texture pack'


class ModTypes:
    @staticmethod
    def __iter__():
        for cls_name, cls in inspect.getmembers(sys.modules[__name__], inspect.isclass):
            if cls_name != ModTypes.__name__ and not inspect.isabstract(cls):
                yield cls

    @staticmethod
    def enum_category_names():
        for cls in sorted(ModTypes.__iter__(), key=lambda x: x().sorting_weight):
            print(cls)
            yield cls().category_name


if __name__ == '__main__':
    # for x in ModTypes():
    #     print(x)
    for x in ModTypes.enum_category_names():
        print(x)
