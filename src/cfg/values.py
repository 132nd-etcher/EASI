# coding=utf-8

import os

import path

from src.meta import meta_property_with_default
from src.sig import sig_author_mode, sig_sg_path_changed, sig_cache_path_changed, sig_kdiff_path_changed


class ConfigValues:
    @meta_property_with_default(False, bool)
    def subscribe_to_test_versions(self, value):
        """Whether or not to update EASI to pre-releases"""

    @meta_property_with_default(None, str)
    def saved_games_path(self, value: str):
        """Path to the Saved Games folder"""
        p = path.Path(value)
        if not p.exists():
            raise FileNotFoundError('path does not exist: {}'.format(p.abspath()))
        elif not p.isdir():
            raise TypeError('path is not a directory: {}'.format(p.abspath()))
        sig_sg_path_changed.send()

    @meta_property_with_default(None, str)
    def active_dcs_installation(self, value: str):
        """DCS installations selected by the user"""

    @meta_property_with_default('', str)
    def usr_name(self, value: str):
        """Name of the user for crash reports"""

    @meta_property_with_default('', str)
    def usr_email(self, value: str):
        """Address used for the"reply_to" in crash reports"""

    @meta_property_with_default(set(), set)
    def ack(self, value: set):
        """List of acknowledged disclaimers & info"""

    @meta_property_with_default(False, bool)
    def author_mode(self, value: bool):
        sig_author_mode.mod_author_changed(value)

    @meta_property_with_default(os.path.abspath('.\cache'), str)
    def cache_path(self, value: str):
        p = path.Path(value)
        if not p.exists():
            os.makedirs(str(p.abspath()))
        elif not p.isdir():
            raise TypeError('there is already a file at: {}'.format(p.abspath()))
        sig_cache_path_changed.send()

    @meta_property_with_default(None, str)
    def kdiff_path(self, value: str):
        p = path.Path(value)
        if not p.exists():
            raise FileNotFoundError('{} does not exist'.format(p.abspath()))
        elif not p.isfile():
            raise ValueError('not a file: {}'.format(p.abspath()))
        elif not p.name == 'kdiff3.exe':
            raise ValueError('expected "kdiff3.exe", got: {} ({})'.format(p.name, p.abspath()))
        sig_kdiff_path_changed.send()
