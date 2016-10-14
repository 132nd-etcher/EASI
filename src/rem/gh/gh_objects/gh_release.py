# coding=utf-8
from src.rem.gh.gh_objects.base_gh_object import BaseGHObject, json_property
from src.rem.gh.gh_objects.gh_asset import GHAllReleaseAssets
from src.rem.gh.gh_objects.gh_user import GHUser


class GHRelease(BaseGHObject):
    @json_property
    def url(self):
        """"""

    @json_property
    def html_url(self):
        """"""

    @json_property
    def assets_url(self):
        """"""

    @json_property
    def tag_name(self):
        """"""

    @json_property
    def name(self):
        """"""

    @json_property
    def draft(self):
        """"""

    @json_property
    def prerelease(self):
        """"""

    @json_property
    def created_at(self):
        """"""

    @json_property
    def published_at(self):
        """"""

    @json_property
    def body(self):
        """"""

    def author(self):
        return GHUser(self.json['author'])

    def assets(self):
        return GHAllReleaseAssets(self.json['assets'])

    @property
    def version(self):
        if self.tag_name is None:
            return None
        return self.tag_name

    @property
    def setup_download_url(self):
        return self.assets()[0].browser_download_url


class GHAllReleases(BaseGHObject):
    def __iter__(self):
        for x in self.json:
            yield GHRelease(x)

    def final_only(self):
        for x in self:
            if not x.prerelease:
                yield x

    def prerelease_only(self):
        for x in self:
            if x.prerelease:
                yield x

    def __getitem__(self, item) -> GHRelease:
        for rel in self:
            if rel.name == item:
                return rel
        raise AttributeError('release not found: {}'.format(item))

    def __len__(self) -> int:
        return len(self.json)

    def __contains__(self, item) -> bool:
        try:
            self.__getitem__(item)
            return True
        except AttributeError:
            return False
