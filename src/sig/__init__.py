# coding=utf-8

from blinker import signal

from .sigmsg import SigMsg
from .sigprogress import SigProgress

SIG_PROGRESS = signal('SigProgress', doc='App-wide progress update signal; src.abstract.progress_interface')
SIG_MSG = signal('SigMsg', doc='App-wide signal sent whenever there\'s a need to notify the user about something')
SIG_LOCAL_MOD_CHANGED = signal('SigLocalModChanged',
                               doc='App-wide signal sent when a local mod is changed, added or deleted')
SIG_LOCAL_REPO_CHANGED = signal('SigLocalRepoChanged',
                                doc='App-wide signal sent when a local repo is changed, added or deleted')
