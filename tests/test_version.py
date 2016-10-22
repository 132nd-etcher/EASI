# coding=utf-8

import semver


def test_semver():
    base = '3.4.5-pre.2+build.4'
    assert semver.bump_patch(base) == '3.4.6'
    assert semver.bump_build(base) == '3.4.5-pre.2+build.5'
    assert semver.bump_prerelease(base) == '3.4.5-pre.3'
    assert semver.compare(base, '3.4.4') == 1
    assert semver.compare(base, '3.4.5-alpha') == 1
    assert semver.compare(base, '3.4.5-beta') == 1
    assert semver.compare('3.4.5-rc.1', '3.4.5-beta.1') == 1
    assert semver.compare('3.4.5-beta.1', '3.4.5-alpha.1') == 1
    assert semver.compare('3.4.5', '3.4.5-alpha.1') == 1
