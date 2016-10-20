# coding=utf-8

import os
from unittest import skipIf
import pytest


@skipIf(os.getenv('APPVEYOR'), 'WIP')
def test_config_init():
    pytest.fail()
