# Update & versionning

## Basics

Updating EASI is as simple as starting it. If, during startup, it detects a newer version, that version will automatically be downloaded and installed.

All files and settings are preserved during updates.

## Update channels

By default, EASI will only update itself to the most stable version (which, at the time I'm writing this, is confusingly still considered an experimental version).

I you so desire, you may elect to subscribe to a different (less stable) channel and receive early updates before they are integrated in the stable branch.

This allows you to enjoy the latest features, and offers me early feedback on potential bugs.

To opt-in for a different update channel, got the settings page (CTRL+S) and look for the dropdown menu in the update section.

### Semantic versionning

EASI follows the convention of [Sementic Versionning 2.0.0][semver].

Versionning is done automatically by [Git Version][gitversion] at build time and written into the resulting [PE][pefile].

The current version of EASI is shown in the main window title-bar.

### Branches & packages

| Channel | Branch           | Description                                      |
| ------- | ---------------- | ------------------------------------------------ |
| alpha   | feat/            | Very early testing of new features               |
| beta    | pull/*           | Early testing of features ready to be integrated |
| dev     | develop          | Development version                              |
| rc      | release/*        | Release candidate                                |
| stable  | master & hotfix/ | Stable version                                   |

## AV artifacts


[av_history]: https://ci.appveyor.com/project/132nd-etcher/easi-t0k6c/history
[semver]: http://semver.org/
[gitversion]: https://github.com/GitTools/GitVersion
[pefile]: https://en.wikipedia.org/wiki/Portable_Executable