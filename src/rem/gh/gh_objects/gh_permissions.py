# coding=utf-8

from src.rem.gh.gh_objects.base_gh_object import BaseGHObject, json_property


class GHPermissions(BaseGHObject):
    @json_property
    def admin(self):
        """"""

    @json_property
    def push(self):
        """"""

    @json_property
    def pull(self):
        """"""
