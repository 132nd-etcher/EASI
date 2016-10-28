# coding=utf-8

import pytest


# noinspection SpellCheckingInspection
@pytest.fixture(params=['SG', 'saved games', 'SAveD_GameS', 'savedgames'])
def valid_destination(request, tmpdir):
    yield request.param
    tmpdir.remove()


# noinspection SpellCheckingInspection
@pytest.fixture(params=['SGG', 's_g', 'saveddgames', 'DCSD', 'ddcs'])
def invalid_destination(request, tmpdir):
    yield request.param
    tmpdir.remove()
