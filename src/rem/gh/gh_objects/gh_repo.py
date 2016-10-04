# coding=utf-8

from src.rem.gh.gh_objects.base_gh_object import BaseGHObject, json_property
from src.rem.gh.gh_objects.gh_user import GHUser
from src.rem.gh.gh_objects.gh_permissions import GHPermissions


class GHRepoList(BaseGHObject):

    def __iter__(self):
        for x in self.json:
            yield GHRepo(x)



class GHRepo(BaseGHObject):

    def owner(self) -> GHUser:
        return GHUser(self.json['owner'])

    def permissions(self):
        return GHPermissions(self.json['permissions'])

    def source(self):
        print(type(self.json))
        if 'source' in self.json.keys():
            return GHRepo(self.json['source'])

    @json_property
    def id(self):
        """"""

    @json_property
    def name(self):
        """"""

    @json_property
    def full_name(self):
        """"""

    @json_property
    def description(self):
        """"""

    @json_property
    def private(self):
        """"""

    @json_property
    def fork(self):
        """"""

    @json_property
    def url(self):
        """"""

    @json_property
    def html_url(self):
        """"""

    @json_property
    def archive_url(self):
        """"""

    @json_property
    def branches_url(self):
        """"""

    @json_property
    def clone_url(self):
        """"""

    @json_property
    def commits_url(self):
        """"""

    @json_property
    def downloads_url(self):
        """"""

    @json_property
    def size(self):
        """"""

    @json_property
    def default_branch(self):
        """"""

    @json_property
    def open_issues_count(self):
        """"""

    @json_property
    def pushed_at(self):
        """"""

    @json_property
    def created_at(self):
        """"""

    @json_property
    def updated_at(self):
        """"""

    @json_property
    def subscribers_count(self):
        """"""

    @json_property
    def tags_url(self):
        """"""