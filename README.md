![image][easi]

# Etcher's Automated Skins Installer

[![Pun][pun]][pun_link]

[![Project Status: WIP - Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.][project_status]](http://www.repostatus.org/#wip)
[![GitHub version][project_version]][project_link]
[![Download count][gh_download]][download_link]

[![Semver 2.0.0][semver]][semver_link]
[![Python version][python_version]](https://www.python.org/)
[![GPL v3][license]] [gpl_link]

## Table of content
  - [Documentation](#documentation)
  * [Building](#building)
  - [License](#license)



|                  | Master                                      | Develop                                     |
| ---------------- | ------------------------------------------- | ------------------------------------------- |
| Waffle           | [![waffle]]             [waffle_link]       |                                             |
| Windows build    | [![appveyor]]           [appveyor_link]     | [![appveyor_dev]]     [appveyor_link]       |
| Codacy           | [![codacy_grade]]       [codacy_link]       | [![codacy_grade_dev]] [codacy_link]         |
|                  | [![codacy_cover]]       [codacy_link]       | [![codacy_cover_dev]] [codacy_link]         |
| Scrutinizer      | [![scrutquality]]       [scrut_master_link] | [![scrutqualitydev]]  [scrut_dev_link]      |
|                  | [![scrutcover]]         [scrutcover_link]   | [![scrutcoverdev]]    [scrutcover_link]     |
| Codecov          | [![codecov]]            [codecov_link]      | [![codecovdev]]       [codecov_link]        |
| Codeclimate      | [![codeclimate]]        [codeclimate_link]  |                                             |
|                  | [![codeclimatecount]]   [codeclimate_link]  |                                             |
| Quantified code  | [![quantified]]         [quantified_link]   | [![quantifieddev]]    [quantified_link]     |
| Coveralls        | [![coveralls]]          [coveralls_link]    |                                             |
| Landscape        | [![landscape]]          [landscape_link]    | [![landscape_dev]]    [landscape_link_dev]  |
| VersionEye       | [![versioneye]]         [versioneye_link]   |                                             |
| Gitter           | [![gitter]]             [gitter_link]       |                                             |

[![throughput]] [waffle_link]

[![gh_issues]] [issues_link]
[![gh_issues_closed]] [issues_closed_link]

[![gh_pr]] [pr_link]
[![gh_pr_closed]] [pr_closed_link]

Documentation
=============

[Project documentation][doc_link]

Requirements
============

This project's dependencies are managed by [VersionEye][versioneye_link]

Building
========

1. Install requirements

    ```cmd
    CMD.EXE>
    pip.exe install -r requirements.txt
    pip.exe install -r requirements-extra.txt
    pip.exe install -r requirements-build.txt
    ```

1. Run tests

    ```cmd
    CMD.EXE>
    pip.exe install -r requirements-test.txt
    pytests -c pytest
    ```

1. Build PyQt5 "\*.ui" files

    ```python
    Python 3.5>
    from PyQt5 import uic
    uic.compileUiDir(<qt_skeleton_dir>, from_imports=True, import_from='src.ui.resources')
    ```

1. Build PyQt5 resource files

    ```cmd
    CMD.EXE>
    pyrcc5.exe qt_resource.qrc -o qt_resource_rc.py
    ```

1. Build with PyInstaller

    `%PYTHON%` is the path to your Python 3.5 executable.

    `%COMPILEKEY%` is the key used to encrypt resulting executable.
    (if you don't want to encrypt the executable, skip the `--key` parameter)

    ```cmd
    CMD.EXE>
    "%PYTHON%/python.exe -m PyInstaller ./src/main.py --noconfirm --onefile --clean --icon src/ui/resources/app.ico --workpath ./build/build --paths %PYTHON%/Lib/site-packages/PyQt5/Qt/bin --name EASI --distpath ./build/dist_windowed --windowed --key %COMPILEKEY%"
    ```

## License

EASI is released under the [GPLv3 License][gpl_link].

[waffle]:             https://img.shields.io/waffle/label/132nd-etcher/easi/in%20progress.svg?maxAge=3600
[waffle_link]:        https://waffle.io/132nd-etcher/EASI
[throughput]:         https://graphs.waffle.io/132nd-etcher/EASI/throughput.svg
[appveyor]:           https://img.shields.io/appveyor/ci/132nd-etcher/easi/master.svg?maxAge=3600
[appveyor_dev]:       https://img.shields.io/appveyor/ci/132nd-etcher/easi/develop.svg?maxAge=3600
[appveyor_link]:      https://ci.appveyor.com/project/132nd-etcher/easi
[codacy_grade]:       https://img.shields.io/codacy/grade/3a1f938dbe5545ad9cfa29b8df61e6ac/master.svg?maxAge=3600
[codacy_grade_dev]:   https://img.shields.io/codacy/grade/3a1f938dbe5545ad9cfa29b8df61e6ac/develop.svg?maxAge=3600
[codacy_cover]:       https://img.shields.io/codacy/coverage/3a1f938dbe5545ad9cfa29b8df61e6ac/master.svg?maxAge=3600
[codacy_cover_dev]:   https://img.shields.io/codacy/coverage/3a1f938dbe5545ad9cfa29b8df61e6ac/develop.svg?maxAge=3600
[codacy_link]:        https://www.codacy.com/app/132nd-etcher/EASI/dashboard
[scrutquality]:       https://scrutinizer-ci.com/g/132nd-etcher/EASI/badges/quality-score.png?b=master
[scrutqualitydev]:    https://scrutinizer-ci.com/g/132nd-etcher/EASI/badges/quality-score.png?b=develop
[scrut_master_link]:  https://scrutinizer-ci.com/g/132nd-etcher/EASI/?branch=master
[scrut_dev_link]:     https://scrutinizer-ci.com/g/132nd-etcher/EASI/?branch=develop
[scrutcover]:         https://scrutinizer-ci.com/g/132nd-etcher/EASI/badges/coverage.png?b=master
[scrutcover_link]:    https://scrutinizer-ci.com/g/132nd-etcher/EASI/?branch=master
[scrutcoverdev]:      https://scrutinizer-ci.com/g/132nd-etcher/EASI/badges/coverage.png?b=develop
[scrutcoverdev_link]: https://scrutinizer-ci.com/g/132nd-etcher/EASI/?branch=develop
[codecov]:            https://codecov.io/gh/132nd-etcher/EASI/branch/master/graph/badge.svg
[codecovdev]:         https://codecov.io/gh/132nd-etcher/EASI/branch/develop/graph/badge.svg
[codecov_link]:       https://codecov.io/gh/132nd-etcher/EASI
[codeclimate]:        https://codeclimate.com/github/132nd-etcher/EASI/badges/gpa.svg?style=flat
[codeclimate_link]:   https://codeclimate.com/github/132nd-etcher/EASI
[codeclimatecount]:   https://codeclimate.com/github/132nd-etcher/EASI/badges/issue_count.svg?style=flat
[quantified]:         https://www.quantifiedcode.com/api/v1/project/c20bff6d0c384ec890e23c8d020ae34a/snapshot/origin:master:HEAD/badge.svg
[quantifieddev]:      https://www.quantifiedcode.com/api/v1/project/c20bff6d0c384ec890e23c8d020ae34a/snapshot/origin:develop:HEAD/badge.svg
[quantified_link]:    https://www.quantifiedcode.com/app/project/c20bff6d0c384ec890e23c8d020ae34a
[coveralls]:          https://coveralls.io/repos/github/132nd-etcher/EASI/badge.svg?branch=HEAD&style=flat
[coveralls_link]:     https://coveralls.io/github/132nd-etcher/EASI?branch=HEAD
[landscape]:          https://landscape.io/github/132nd-etcher/EASI/master/landscape.svg?style=flat
[landscape_link]:     https://landscape.io/github/132nd-etcher/EASI/master
[landscape_dev]:      https://landscape.io/github/132nd-etcher/EASI/develop/landscape.svg?style=flat
[landscape_link_dev]: https://landscape.io/github/132nd-etcher/EASI/develop
[versioneye]:         https://www.versioneye.com/user/projects/57ff67d90676c900486e4f8d/badge.svg?style=flat
[versioneye_link]:    https://www.versioneye.com/user/projects/57ff67d90676c900486e4f8d
[gitter]:             https://badges.gitter.im/easi_/Lobby.svg
[gitter_link]:        https://gitter.im/easi_/Lobby
[license]:            https://img.shields.io/github/license/132nd-etcher/easi.svg?maxAge=3600
[gpl_link]:           https://www.gnu.org/licenses/quick-guide-gplv3.en.html
[easi]:               https://i.imgsafe.org/00192c67ea.png
[project_status]:     http://www.repostatus.org/badges/latest/wip.svg
[pun]:                https://img.shields.io/badge/Author%20skill-Script%20kiddie-red.svg?style=flat
[pun_link]:           http://users.telenet.be/mydotcom/graph/geek.jpg
[semver]:             https://img.shields.io/badge/semver-2.0.0-blue.svg
[semver_link]:        http://semver.org/
[doc_link]:           http://semver.org/
[issues_link]:        https://github.com/132nd-etcher/EASI/issues
[issues_closed_link]: https://github.com/132nd-etcher/EASI/issues?q=is%3Aissue+is%3Aclosed
[pr_link]:            https://github.com/132nd-etcher/EASI/pulls
[pr_closed_link]:     https://github.com/132nd-etcher/EASI/pulls?q=is%3Apr+is%3Aclosed



[gh_download]:        https://img.shields.io/github/downloads/132nd-etcher/easi/total.svg?maxAge=3600
[download_link]:      https://github.com/132nd-etcher/EASI/releases
[gh_issues]:          https://img.shields.io/github/issues/132nd-etcher/easi.svg?maxAge=3600
[gh_issues_closed]:   https://img.shields.io/github/issues-closed/132nd-etcher/easi.svg?maxAge=3600
[gh_pr]:              https://img.shields.io/github/issues-pr/132nd-etcher/easi.svg?maxAge=3600
[gh_pr_closed]:       https://img.shields.io/github/issues-pr-closed/132nd-etcher/easi.svg?maxAge=3600
[gh_release]:         https://img.shields.io/github/release/132nd-etcher/easi.svg?maxAge=3600
[project_version]:    https://badge.fury.io/gh/132nd-etcher%2Feasi.svg
[project_link]:        https://github.com/132nd-etcher/EASI
[python_version]:     https://img.shields.io/badge/python-3.5-blue.svg
