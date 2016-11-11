# coding=utf-8

from re import compile

DCS_VERSION_REGEX = r'^([0-9]+(\.([0-9]+(\.([0-9]+(\.([0-9]{5,}|\*))?|\*))?|\*))?|\*)+(\+)?$'
RE_DCS_VERSION = compile(DCS_VERSION_REGEX)


class DCSVersion:

    @staticmethod
    def is_valid(dcs_version: str) -> bool:
        return RE_DCS_VERSION.match(dcs_version) is not None
