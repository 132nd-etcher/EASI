# coding=utf-8

import os

import path

from src.meta.decorators import MetaPropertyWithDefault
from src.sig import sig_cfg_author_mode, sig_cfg_sg_path, sig_cfg_cache_path, sig_cfg_kdiff_path,\
    sig_cfg_keyring_encrypt, sig_cfg_active_dcs_install, sig_cfg_user_name, sig_cfg_user_mail,\
    sig_cfg_subscribe_to_test_versions


class ConfigValues:
    @MetaPropertyWithDefault(False, bool)
    def subscribe_to_test_versions(self, value):
        sig_cfg_subscribe_to_test_versions.value_changed(value)

    @MetaPropertyWithDefault(None, str)
    def saved_games_path(self, value: str):
        """Path to the Saved Games folder"""
        p = path.Path(value)
        if not p.exists():
            raise FileNotFoundError('path does not exist: {}'.format(p.abspath()))
        elif not p.isdir():
            raise TypeError('path is not a directory: {}'.format(p.abspath()))
        sig_cfg_sg_path.value_changed(value)

    @MetaPropertyWithDefault(None, str)
    def active_dcs_installation(self, value: str):
        sig_cfg_active_dcs_install.value_changed(value)

    @MetaPropertyWithDefault('', str)
    def usr_name(self, value: str):
        sig_cfg_user_name.value_changed(value)

    @MetaPropertyWithDefault('', str)
    def usr_email(self, value: str):
        sig_cfg_user_mail.value_changed(value)

    @MetaPropertyWithDefault(set(), set)
    def ack(self, value: set):
        """List of acknowledged disclaimers & info"""

    @MetaPropertyWithDefault(False, bool)
    def author_mode(self, value: bool):
        sig_cfg_author_mode.value_changed(value)

    @MetaPropertyWithDefault(False, bool)
    def encrypt_keyring(self, value: bool):
        sig_cfg_keyring_encrypt.value_changed(value)

    @MetaPropertyWithDefault(os.path.abspath(r'.\cache'), str)
    def cache_path(self, value: str):
        p = path.Path(value)
        if not p.exists():
            os.makedirs(str(p.abspath()))
        elif not p.isdir():
            raise TypeError('there is already a file at: {}'.format(p.abspath()))
        sig_cfg_cache_path.value_changed(value)

    @MetaPropertyWithDefault(os.path.abspath(r'.\kdiff3\kdiff3.exe'), str)
    def kdiff_path(self, value: str):
        p = path.Path(value)
        if not p.exists():
            raise FileNotFoundError('{} does not exist'.format(p.abspath()))
        elif not p.isfile():
            raise ValueError('not a file: {}'.format(p.abspath()))
        elif not p.name == 'kdiff3.exe':
            raise ValueError('expected "kdiff3.exe", got: {} ({})'.format(p.name, p.abspath()))
        sig_cfg_kdiff_path.value_changed(value)
