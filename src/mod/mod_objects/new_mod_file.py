# coding=utf-8
from src.low.custom_path import Path


class UnknownDestination(Exception):
    """"""


class SrcModFile:
    # noinspection SpellCheckingInspection
    known_destinations = dict(
        saved_games=['sg', 'saved games', 'saved_games', 'savedgames']
    )

    special_files_handlers = {
        'autoexec.cfg': None,
        'description.lua': None
    }

    def __init__(self, src, root):
        assert isinstance(src, Path)
        self.__path = src
        self.__dest, self.__relpath = self.verify_destination(root)

    @property
    def path(self) -> Path:
        return self.__path

    @property
    def dest(self) -> str:
        return self.__dest

    @property
    def relpath(self):
        return self.__relpath

    @property
    def filename(self):
        return self.path.basename()

    def __str__(self):
        return '{}: {} -> {} ({})'.format(self.filename, self.path.abspath(), self.dest, self.relpath)

    def verify_destination(self, root):
        destination = self.path.relpath(root)
        for known_destination, acceptable_values in self.known_destinations.items():
            if destination.lower().split('\\')[0] in acceptable_values:
                return known_destination, destination.lower().replace(destination.lower().split('\\')[0], '')
        raise UnknownDestination(destination)