# coding=utf-8
import unittest

import semver


class TestSemver(unittest.TestCase):
    def setUp(self):
        pass

    def test_semver(self):
        base = '3.4.5-pre.2+build.4'
        self.assertSequenceEqual(
            semver.bump_patch(base),
            '3.4.6'
        )
        self.assertSequenceEqual(
            semver.bump_build(base),
            '3.4.5-pre.2+build.5'
        )
        self.assertSequenceEqual(
            semver.bump_prerelease(base),
            '3.4.5-pre.3'
        )
        self.assertEqual(
            semver.compare(
                base,
                '3.4.4'),
            1
        )
        self.assertEqual(
            semver.compare(
                base,
                '3.4.5-alpha'),
            1
        )
        self.assertEqual(
            semver.compare(
                base,
                '3.4.5-beta'),
            1
        )
        self.assertEqual(
            semver.compare(
                '3.4.5-rc.1',
                '3.4.5-beta.1'),
            1
        )
        self.assertEqual(
            semver.compare(
                '3.4.5-beta.1',
                '3.4.5-alpha.1'),
            1
        )
        self.assertEqual(
            semver.compare(
                '3.4.5',
                '3.4.5-alpha.1'),
            1
        )
