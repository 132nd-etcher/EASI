# coding=utf-8

from path import Path

from src.helper.abstract import AbstractHelper

PORTABLE_GIT_LINK = r'https://github.com/git-for-windows/git/releases/download/v2.10.0.windows.1/' \
                    r'PortableGit-2.10.0-32-bit.7z.exe'


class GitHelper(AbstractHelper):
    @property
    def path(self) -> Path:
        return ''

    def install(self, wait: bool = True):
        pass

    @property
    def folder(self):
        return ''

    @property
    def is_installed(self):
        return False

    @property
    def name(self):
        return 'Git'

    def __init__(self):
        AbstractHelper.__init__(self)
        self.__path = None

    @property
    def download_link(self):
        return PORTABLE_GIT_LINK

    @property
    def directory(self):
        return 'portable-git'

    @property
    def executable(self):
        return None
