# coding=utf-8

from .base_bt_object import BaseBTObject, json_property


class BTVersion(BaseBTObject):
    @json_property
    def name(self):
        """"""

    @json_property
    def desc(self):
        """"""

    @json_property
    def package(self):
        """"""

    @json_property
    def repo(self):
        """"""

    @json_property
    def owner(self):
        """"""

    @json_property
    def created(self):
        """"""

    @json_property
    def updated(self):
        """"""

    @json_property
    def github_release_notes_file(self):
        """"""

    @json_property
    def github_use_tag_release_notes(self):
        """"""

    @json_property
    def vcs_tag(self):
        """"""

    @json_property
    def ordinal(self):
        """"""

    @json_property
    def attributes(self):
        """"""


class BTAllVersions(BaseBTObject):
    def __iter__(self):
        for x in self.json:
            yield BTVersion(x)

    def __getitem__(self, item) -> BTVersion:
        for file in self:
            if file.name == item:
                return file
        raise AttributeError('release not found: {}'.format(item))

    def __len__(self) -> int:
        return len(self.json)

    def __contains__(self, file) -> bool:
        try:
            self.__getitem__(file)
            return True
        except AttributeError:
            return False
