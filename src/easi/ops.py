# coding=utf-8

import typing

from src.low.custom_path import Path


# noinspection PyUnusedLocal
def dummy(*args, **kwargs):
    raise RuntimeError('confirm not initialized')


_confirm_func = dummy
_select_func = dummy
_simple_input = dummy
_long_input = dummy
_get_dcs_version = dummy
_warn_func = dummy
_get_directory = dummy
_save_file = dummy
_get_existing_file = dummy
_get_existing_files = dummy
_get_file = dummy
_get_new_gh_login = dummy
_create_new_mod_collect_basics = dummy


def confirm(question: str, title: str = 'Please confirm', parent=None) -> bool:
    return _confirm_func(question, title, parent)


def select(choices: list, title: str, text: str = '', default=None, help_link=None, parent=None):
    return _select_func(choices, title, text, default, help_link, parent)


def warn(_id: str, text: str, title: str = None, buttons: str = None, parent=None):
    return _warn_func(_id, text, title, buttons, parent)


def simple_input(title: str, text: str = '', default: str = '', verify_input_func=None, help_link=None, parent=None):
    return _simple_input(title, text, default, verify_input_func, help_link, parent)


def long_input(title: str, text: str = '', default: str = '', verify_input_func=None, help_link=None, parent=None):
    return _long_input(title, text, default, verify_input_func, help_link, parent)


def get_dcs_version(title: str, text: str, default: str = '', help_link=None, parent=None):
    return _get_dcs_version(title, text, default, help_link, parent)


def get_directory(parent, title: str, init_dir: str = '.') -> Path or None:
    return _get_directory(parent, title, init_dir)


def save_file(parent, title: str, _filter: typing.List[str] = None, init_dir: str = '.') -> Path or None:
    return _save_file(parent, title, _filter, init_dir)


def get_existing_file(parent, title: str, _filter: typing.List[str] = None, init_dir: str = '.') -> Path or None:
    return _get_existing_file(parent, title, _filter, init_dir)


def get_existing_files(
        parent,
        title: str,
        _filter: typing.List[str] = None,
        init_dir: str = '.') -> typing.List[Path] or None:
    return _get_existing_files(parent, title, _filter, init_dir)


def get_file(parent, title: str, _filter: typing.List[str] = None, init_dir: str = '.') -> Path or None:
    return _get_file(parent, title, _filter, init_dir)


def get_new_gh_login(parent=None):
    return _get_new_gh_login(parent)


def create_new_mod_collect_basics(parent=None):
    return _create_new_mod_collect_basics(parent)
