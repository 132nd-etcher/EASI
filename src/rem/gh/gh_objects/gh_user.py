# coding=utf-8


from .base_gh_object import BaseGHObject, json_property

class GHUser(BaseGHObject):

    @json_property
    def login(self):
        """"""

    @json_property
    def html_url(self):
        """"""

    @json_property
    def url(self):
        """"""

    @json_property
    def id(self):
        """"""