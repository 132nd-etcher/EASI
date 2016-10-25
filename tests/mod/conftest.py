# coding=utf-8

import pytest


# noinspection SpellCheckingInspection
@pytest.fixture(params=['SG', 'saved games', 'SAveD_GameS', 'savedgames'])
def valid_destination(request, tmpdir):
    yield request.param
    tmpdir.remove()
