# coding=utf-8

from .kdiff import kdiff


def init_helpers():
    if not kdiff.is_installed:
        kdiff.install()
