![image][easi]

# Etcher's Automated Skins Installer

![][project_status] ![][license] ![][pun] ![][gh_download] ![][semver]

  - [Documentation](#documentation)
  - [Building](#building)
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

![][gh_issues]
![][gh_issues_closed]
![][gh_pr]
![][gh_pr_closed]

Documentation
=============

[Project documentation](https://132nd-etcher.github.io/EASI/)

Building
========

1. Install requirements

    ```cmd
    > pip.exe install -r requirements.txt
    > pip.exe install -r requirements-extra.txt
    > pip.exe install -r requirements-build.txt
    ```

1. Build PyQt5 "\*.ui" files

    ```python
    from PyQt5 import uic
    uic.compileUiDir(<qt_skeleton_dir>, from_imports=True, import_from='src.ui.resources')
    ```

1. Build PyQt5 resource files

    ```cmd
    > pyrcc5.exe qt_resource.qrc -o qt_resource_rc.py
    ```

1. Build with PyInstaller

    ```cmd
    > "%PYTHON%/python.exe -m PyInstaller ./src/main.py --noconfirm --onefile --clean --icon src/ui/resources/app.ico --workpath ./build/build --paths %PYTHON%/Lib/site-packages/PyQt5/Qt/bin --name EASI --distpath ./build/dist_windowed --windowed --key %COMPILEKEY%"
    ```
    
## License

EASI is released under the [GPLv3 License][gpl_link].

![license]

[waffle]:             https://img.shields.io/waffle/label/132nd-etcher/easi/in%20progress.svg?maxAge=86400
[waffle_link]:        https://waffle.io/132nd-etcher/EASI
[throughput]:         https://graphs.waffle.io/132nd-etcher/EASI/throughput.svg
[appveyor]:           https://img.shields.io/appveyor/ci/132nd-etcher/easi/master.svg?maxAge=86400
[appveyor_dev]:       https://img.shields.io/appveyor/ci/132nd-etcher/easi/develop.svg?maxAge=86400
[appveyor_link]:      https://ci.appveyor.com/project/132nd-etcher/easi
[codacy_grade]:       https://img.shields.io/codacy/grade/3a1f938dbe5545ad9cfa29b8df61e6ac/master.svg?maxAge=86400
[codacy_grade_dev]:   https://img.shields.io/codacy/grade/3a1f938dbe5545ad9cfa29b8df61e6ac/develop.svg?maxAge=86400
[codacy_cover]:       https://img.shields.io/codacy/coverage/3a1f938dbe5545ad9cfa29b8df61e6ac/master.svg?maxAge=86400
[codacy_cover_dev]:   https://img.shields.io/codacy/coverage/3a1f938dbe5545ad9cfa29b8df61e6ac/develop.svg?maxAge=86400
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
[license]:            https://img.shields.io/github/license/132nd-etcher/easi.svg?maxAge=86400
[gpl_link]:           https://www.gnu.org/licenses/quick-guide-gplv3.en.html
[easi]:               https://i.imgsafe.org/00192c67ea.png
[project_status]:     http://www.repostatus.org/badges/latest/wip.svg
[pun]:                https://img.shields.io/badge/Author%20skill-Script%20kiddie-red.svg?style=flat
[semver]:             https://img.shields.io/badge/semver-2.0.0-blue.svg

[gh_download]:        https://img.shields.io/github/downloads/132nd-etcher/easi/total.svg?maxAge=86400
[gh_issues]:          https://img.shields.io/github/issues/132nd-etcher/easi.svg?maxAge=86400
[gh_issues_closed]:   https://img.shields.io/github/issues-closed/132nd-etcher/easi.svg?maxAge=86400
[gh_pr]:              https://img.shields.io/github/issues-pr/132nd-etcher/easi.svg?maxAge=86400
[gh_pr_closed]:       https://img.shields.io/github/issues-pr-closed/132nd-etcher/easi.svg?maxAge=86400
[gh_release]:         https://img.shields.io/github/release/132nd-etcher/easi.svg?maxAge=86400