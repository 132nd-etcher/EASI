# coding=utf-8

import re


class Version:
    """
    Represents a version as major.minor.revision.build, where each one is an int
    """

    def __init__(self, version_str: str = None, major: int = None, minor: int = None, revision: int = None,
                 build: int = None):
        if version_str is not None:
            if not isinstance(version_str, str):
                raise ValueError('expected a str, got: {}'.format(type(version_str)))
            self.__version_str = version_str
            pattern = re.compile(r'^(?P<major>[0-9]+)\.(?P<minor>[0-9]+)\.(?P<revision>[0-9]+)\.(?P<build>[0-9]+)$')
            try:
                m = pattern.match(version_str)
            except TypeError:
                raise ValueError('invalid version string: {}'.format(version_str))
            else:
                if not m:
                    raise ValueError('invalid version string: {}'.format(version_str))
                else:
                    self.__major = m.group('major')
                    self.__minor = m.group('minor')
                    self.__revision = m.group('revision')
                    self.__build = m.group('build')
        else:
            params = [major, minor, revision, build]
            if all([p is not None for p in params]):
                for p in params:
                    if not isinstance(p, int) or p < 0:
                        raise ValueError('expected a positive int, got "{}" instead'.format(type(p)))
                self.__major = major
                self.__minor = minor
                self.__revision = revision
                self.__build = build
            else:
                raise ValueError('yo parameters are fucked up, mama: {}'.format(params))

    def reset_build(self):
        """
        Sets "build" to 0
        """
        self.__build = '0'

    def reset_revision(self):
        """
        Sets "revision" to 0
        """
        self.__revision = '0'

    def reset_minor(self):
        """
        Sets "minor" to 0
        """
        self.__minor = '0'

    def bump_build(self):
        """
        Bumps "build"
        """
        self.__build = str(self.build + 1)

    def bump_revision(self):
        """
        Bumps "revision"
        """
        self.__revision = str(self.revision + 1)

    def bump_minor(self):
        """
        Bumps "minor"
        """
        self.__minor = str(self.minor + 1)

    def bump_major(self):
        """
        Bumps "major"
        """
        self.__major = str(self.major + 1)

    @property
    def major(self):
        """Returns: major part of the Version as an int"""
        return int(self.__major)

    @property
    def minor(self):
        """Returns: minor part of the Version as an int"""
        return int(self.__minor)

    @property
    def revision(self):
        """Returns: revision part of the Version as an int"""
        return int(self.__revision)

    @property
    def build(self):
        """Returns: build part of the Version as an int"""
        return int(self.__build)

    def to_tuple(self):
        """
        :return: tuple of elements as major, minor, revision, build
        """
        return self.major, self.minor, self.revision, self.build

    def __str__(self):
        return '{}.{}.{}.{}'.format(self.major, self.minor, self.revision, self.build)

    def __repr__(self):
        return 'Version(\'{}\')'.format(self.__version_str)

    def __eq__(self, other):
        return all([self.major == other.major, self.minor == other.minor, self.build == other.build,
                    self.revision == other.revision])

    def __lt__(self, other):
        if self.major < other.major:
            return True
        elif self.major > other.major:
            return False
        if self.minor < other.minor:
            return True
        elif self.minor > other.minor:
            return False
        if self.revision < other.revision:
            return True
        elif self.revision > other.revision:
            return False
        if self.build < other.build:
            return True

    def __gt__(self, other):
        return not self.__lt__(other) and not self.__eq__(other)
