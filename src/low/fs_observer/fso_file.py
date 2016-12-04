# coding=utf-8
import stat

from src.low.custom_path import Path


class FSOFile:
    def __init__(
            self,
            name: str,
            abspath: str,
            path: str,
            st,
            isdir: bool,
    ):
        self.isdir = isdir
        self.size = st.st_size
        self.atime = st.st_atime
        self.mtime = st.st_mtime
        self.ctime = st.st_ctime
        self.read_only = bool(stat.FILE_ATTRIBUTE_READONLY & st.st_file_attributes)
        self.hidden = bool(stat.FILE_ATTRIBUTE_HIDDEN & st.st_file_attributes)
        self.system = bool(stat.FILE_ATTRIBUTE_SYSTEM & st.st_file_attributes)
        self.archive = bool(stat.FILE_ATTRIBUTE_ARCHIVE & st.st_file_attributes)
        self.path = path
        self.abspath = abspath
        self.name = name
        self.__crc32 = None

    def __str__(self):
        return '\n\t\t'.join(['{}: {}'.format(k, getattr(self, k)) for k in self.__dict__])

    @property
    def crc32(self) -> str or None:
        if self.__crc32 is None:
            self.get_crc32()
        return self.__crc32

    @crc32.setter
    def crc32(self, value: str):
        self.__crc32 = value

    def get_crc32(self):
        p = Path(self.abspath)
        if p.isfile():
            self.__crc32 = p.crc32()
        else:
            self.__crc32 = 0
