# coding=utf-8

from re import compile


class DCSVersion:
    re_DCS_VERSION = compile(r'^([0-9]+(\.([0-9]+(\.([0-9]+(\.([0-9]{5,}|\*))?|\*))?|\*))?|\*)+(\+)?$')

    @staticmethod
    def is_valid(dcs_version: str) -> bool:
        return DCSVersion.re_DCS_VERSION.match(dcs_version) is not None
