# Feedback

I value your feedback a lot, and I've tried to make it as easy as possible for you to send it to me.

There are multiple ways to send me your thoughts:

### Method 1: via EASI itself (prefered method)

There's a `Feedback` option in the `Help` menu of EASI's main window.

This feedback dialog can be used to ask questions, request help, report bug, or simply contact me.

### Method 2: via the Github repository

If you have a Github account, you can also directly report an issue via [EASI's repository][ghrepo].

## Automated crash reporting

I know that collecting logs, zipping them and sending them in a mail is a tedious process that most of us don't want to go through each time some random freeware crashes.

It helps the developper a lot, though, and most corner-case bugs would never be found without the feedback of the end-user, i.e. you.

That is why I've chosen to implement an automated crash-reporting service into EASI: whenever something goes wrong during the execution of the program, EASI will try to send me a detailed crah report.

#### Personal information handling

EASI will __never__ send any personal information along with its crash-report, except for the bits you willingly provide (like your alias/e-mail).

That being said, there may be pieces of personal information contained in the file paths, e.g. the user name of the `c:\users\<username>\some\file` path.

Automated crash-reporting cannot be disabled for the time being, so if you are not comfortable with EASI sending me these, please don't use it until the feature can be turned off.

[ghrepo]: https://www.github.com/132nd-etcher/EASI