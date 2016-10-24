# coding=utf-8


def init_helpers():
    from .kdiff import kdiff
    if not kdiff.is_installed:
        kdiff.download_and_install()
