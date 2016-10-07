# coding=utf-8

from path import Path

from src.helper.abstract import AbstractHelper

PORTABLE_GIT_LINK = r'https://github.com/git-for-windows/git/releases/download/v2.10.0.windows.1/' \
                    r'PortableGit-2.10.0-32-bit.7z.exe'


class GitHelper(AbstractHelper):
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
        if self.__path is None:
            self.__path = Path(self.helper_dir).joinpath(self.directory).joinpath('git.exe')
        return self.__path
