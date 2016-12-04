# coding=utf-8

from abc import abstractmethod, abstractproperty
from src.rem.gh.gh_anon import GHRepo
from src.git.wrapper import GitRepository
from src.low.custom_path import Path




class IRepo:

    @abstractmethod
    def _clone_from_github(self, user):
        """"""

    @abstractmethod
    def _gather_local_mods(self):
        """"""

    @abstractmethod
    def refresh_mods(self):
        """"""

    @abstractproperty
    def github_url(self) -> str:
        """"""

    @abstractmethod
    def mod_name_is_available(self, mod_name: str) -> bool:
        """"""

    @abstractmethod
    def create_new_mod(self, mod_name: str):
        """"""

    @abstractmethod
    def trash_mod(self, mod_name: str):
        """"""

    @abstractproperty
    def local(self) -> GitRepository:
        """"""

    @abstractproperty
    def remote(self) -> GHRepo:
        """"""

    @abstractproperty
    def user_name(self) -> str:
        """"""

    @abstractproperty
    def mods(self) -> set:
        """"""

    @abstractproperty
    def local_git_repo_path(self) -> Path:
        """"""

    @abstractproperty
    def name(self) -> str:
        """"""

    @abstractproperty
    def has_changed(self) -> bool:
        """"""

    @abstractproperty
    def push_perm(self) -> bool:
        """"""

    @abstractproperty
    def owner(self) -> str:
        """"""


