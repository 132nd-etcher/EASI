# coding=utf-8

import pytest

from src.low.custom_path import Path
from src.mod.mod_objects.new_mod_file import UnknownDestination, SrcModFile


def test_path(valid_destination, tmpdir):
    p = str(tmpdir.mkdir(valid_destination).mkdir('sub').join('f'))
    f = SrcModFile(Path(p), str(tmpdir))
    assert f.path == p


def test_dest(valid_destination, tmpdir):
    p = str(tmpdir.mkdir(valid_destination).mkdir('sub').join('f'))
    f = SrcModFile(Path(p), str(tmpdir))
    assert f.dest == 'saved_games'


def test_filename(valid_destination, tmpdir):
    p = str(tmpdir.mkdir(valid_destination).mkdir('sub').join('f'))
    f = SrcModFile(Path(p), str(tmpdir))
    assert f.filename == 'f'


def test_relpath(valid_destination, tmpdir):
    p = str(tmpdir.mkdir(valid_destination).mkdir('sub').join('f'))
    f = SrcModFile(Path(p), str(tmpdir))
    assert f.relpath == r'\sub\f'


def test_wrong_dest(invalid_destination, tmpdir):
    # noinspection SpellCheckingInspection
    p = str(tmpdir.mkdir(invalid_destination).mkdir('sub').join('f'))
    with pytest.raises(UnknownDestination):
        SrcModFile(Path(p), str(tmpdir))
