# coding=utf-8

import os
from unittest import skipIf
import pytest


@skipIf(os.getenv('APPVEYOR'), 'AppVeyor gets 403 from GH all the time')
def test_config_init():
    pytest.fail()
