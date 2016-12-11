# coding=utf-8

import pytest
import os

from src.low.custom_path import Path
from src.new_mod.mod import Mod, ModMeta
from src.new_mod.mod_factory import ModFactory
from src.repo.irepo import IRepo, GHRepo, GitRepository
from src.cache.cache import Cache


class DummyRepo(IRepo):

    def __init__(self, root_dir):
        self._root_dir = root_dir

    def _clone_from_github(self, user):
        pass

    @property
    def remote(self) -> GHRepo:
        return GHRepo({'name': 'repo'})

    @property
    def name(self) -> str:
        return 'repo'

    def trash_mod(self, mod_name: str):
        pass

    def _gather_local_mods(self):
        pass

    @property
    def github_url(self) -> str:
        return 'github_url'

    @property
    def local_git_repo_path(self) -> Path:
        return Path(self._root_dir)

    def refresh_mods(self):
        pass

    @property
    def owner(self) -> str:
        return 'owner'

    @property
    def push_perm(self) -> bool:
        return False

    @property
    def mods(self) -> set:
        return set()

    @property
    def has_changed(self) -> bool:
        return False

    def create_new_mod(self, mod_name: str):
        pass

    @property
    def user_name(self) -> str:
        return 'user_name'

    def mod_name_is_available(self, mod_name: str) -> bool:
        return True

    @property
    def local(self) -> GitRepository:
        return GitRepository(self._root_dir)


@pytest.fixture()
def dummy_mod(tmpdir):
    dummy_repo = DummyRepo(str(tmpdir))
    new_mod = ModFactory.create_new_mod(dummy_repo, 'mod_name')
    assert isinstance(new_mod, Mod)
    yield new_mod, dummy_repo, tmpdir


def test_mod_creation(tmpdir):
    tmpdir = Path(str(tmpdir))
    dummy_repo = DummyRepo(tmpdir.abspath())
    new_mod = ModFactory.create_new_mod(dummy_repo, 'mod_name')
    assert new_mod.meta.name == 'mod_name'
    assert isinstance(new_mod.meta.uuid, str)
    assert Path(new_mod.meta.path).exists() is False
    new_mod.meta.write()
    assert Path(new_mod.meta.path).exists() is True


def test_meta_repo(dummy_mod):
    mod, repo, _ = dummy_mod
    assert mod.meta_repo is repo


def test_mod_meta(dummy_mod):
    mod, _, _ = dummy_mod
    assert isinstance(mod.meta, ModMeta)
    meta = mod.meta
    for attr in ['name', 'uuid', 'author', 'category', 'dcs_version', 'description']:
        assert getattr(meta, attr) == getattr(mod, attr)


def test_local_folder(dummy_mod):
    mod, repo, tmpdir = dummy_mod
    assert mod.local_folder == Path(str(tmpdir)).joinpath('mods', repo.name, mod.meta.name)


def test_mod_rename(dummy_mod):
    mod, _, _ = dummy_mod
    old_meta_path = mod.meta.path
    old_local_folder = mod.local_folder
    assert isinstance(old_meta_path, Path)
    mod.meta.write()
    assert old_meta_path.exists() is True
    assert old_local_folder.exists() is True
    mod.rename('new_name')
    assert old_meta_path.exists() is False
    assert old_local_folder.exists() is False


def test_has_changed(dummy_mod, mocker, qtbot):
    progress_mock = mocker.patch('src.new_mod.mod.SigProgress')
    mod, _, tmpdir = dummy_mod
    assert Cache().path == str(tmpdir)
    assert mod.has_changed is False
    test_file = Path(mod.local_folder.joinpath('some_file'))
    assert os.path.exists(test_file.abspath()) is False
    test_file.write_text('content')
    assert os.path.exists(test_file.abspath()) is True
    assert len(mod.local_files) > 0
    assert mod.has_changed is True



