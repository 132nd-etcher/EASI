# coding=utf-8

from .base_bt_object import BaseBTObject, json_property


class BTFile(BaseBTObject):
    @json_property
    def name(self):
        """"""

    @json_property
    def size(self):
        """"""

    @json_property
    def created(self):
        """"""

    @json_property
    def owner(self):
        """"""

    @json_property
    def repo(self):
        """"""

    @json_property
    def version(self):
        """"""

    @json_property
    def package(self):
        """"""

    @json_property
    def path(self):
        """"""

    @json_property
    def sha1(self):
        """"""


class BTAllFiles(BaseBTObject):
    def __iter__(self):
        for x in self.json:
            yield BTFile(x)

    def __getitem__(self, item) -> BTFile:
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
