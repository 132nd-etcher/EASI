# coding=utf-8

import pytest

from src.abstract.ui.base_dialog import AbstractBaseDialog
from src.abstract.ui.base_qobject import AbstractBaseQWidget
from src.qt import QObject, QIcon, QLabel


def test_wrong_init():
    for x in [QObject, QLabel, QIcon, 'test', True, None, 32]:
        with pytest.raises(TypeError):
            AbstractBaseDialog(x)
        with pytest.raises(TypeError):
            AbstractBaseQWidget(x)
