# coding=utf-8

import os

import path

from src.meta.meta_property import MetaProperty


class ConfigValues:
    @MetaProperty(False, bool)
    def subscribe_to_test_versions(self, value):
        """"""

    @MetaProperty(None, str)
    def saved_games_path(self, value: str):
        """Path to the Saved Games folder"""
        p = path.Path(value)
        if not p.exists():
            raise FileNotFoundError('path does not exist: {}'.format(p.abspath()))
        elif not p.isdir():
            raise TypeError('path is not a directory: {}'.format(p.abspath()))

    @MetaProperty(None, str)
    def active_dcs_installation(self, value: str):
        """"""

    @MetaProperty('', str)
    def usr_name(self, value: str):
        """"""

    @MetaProperty('', str)
    def usr_email(self, value: str):
        """"""

    @MetaProperty(set(), set)
    def to_del(self, value: set):
        """"""

    @MetaProperty(set(), set)
    def ack(self, value: set):
        """List of acknowledged disclaimers & info"""

    @MetaProperty(False, bool)
    def author_mode(self, value: bool):
        """"""

    @MetaProperty(False, bool)
    def encrypt_keyring(self, value: bool):
        """"""

    @MetaProperty(os.path.abspath(r'.\cache'), str)
    def cache_path(self, value: str):
        p = path.Path(value)
        if not p.exists():
            os.makedirs(str(p.abspath()))
        elif not p.isdir():
            raise TypeError('there is already a file at: {}'.format(p.abspath()))

    @MetaProperty(os.path.abspath(r'.\kdiff3\kdiff3.exe'), str)
    def kdiff_path(self, value: str):
        p = path.Path(value)
        if not p.exists():
            raise FileNotFoundError('{} does not exist'.format(p.abspath()))
        elif not p.isfile():
            raise ValueError('not a file: {}'.format(p.abspath()))
        elif not p.name == 'kdiff3.exe':
            raise ValueError('expected "kdiff3.exe", got: {} ({})'.format(p.name, p.abspath()))
