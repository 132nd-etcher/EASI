# coding=utf-8

import pytest
from shortuuid import uuid


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


@pytest.fixture(params=[uuid(), uuid(), uuid(), uuid(), uuid(), uuid()])
def random_mod_name(request, tmpdir):
    yield request.param
    tmpdir.remove()

