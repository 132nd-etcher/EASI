# coding=utf-8

import abc


class AbstractPalette(metaclass=abc.ABCMeta):
    @property
    @abc.abstractproperty
    def note(self) -> str:
        """"""

    @property
    @abc.abstractproperty
    def warning(self) -> str:
        """"""

    @property
    @abc.abstractproperty
    def error(self) -> str:
        """"""

    @property
    @abc.abstractproperty
    def info(self) -> str:
        """"""

    @property
    @abc.abstractproperty
    def background(self) -> str:
        """"""


class PaletteBalloon(AbstractPalette):
    __slots__ = []
    note = 'rgb(236, 208, 120)'
    warning = 'rgb(217, 91, 67)'
    error = 'rgb(192, 41, 66)'
    background = 'rgb(84, 36, 55)'
    info = 'rgb(83, 119, 122)'


class PaletteBalloonFive(AbstractPalette):
    __slots__ = []
    note = 'rgb(237, 201, 81)'
    warning = 'rgb(235, 104, 65)'
    error = 'rgb(204, 51, 63)'
    background = 'rgb(106, 74, 60)'
    info = 'rgb(0, 160, 176)'
