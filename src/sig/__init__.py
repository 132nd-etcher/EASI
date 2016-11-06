# coding=utf-8

from blinker import signal

from .sigmsg import SigMsg
from .sigprogress import SigProgress

SIG_PROGRESS = signal('SigProgress', doc='App-wide progress update signal; src.abstract.progress_interface')
SIG_MSG = signal('SigMsg', doc='Triggers a msgbox or an alternative way of letting the user know about something')

SIG_LOCAL_MOD_CHANGED = signal('SigLocalModChanged',
                               doc='App-wide signal sent when a local mod is changed, added or deleted')
SIG_LOCAL_REPO_CHANGED = signal('SigLocalRepoChanged', doc='')

SIG_CREDENTIALS_GH_CHANGED = signal('SigGHCredentialsChanged', doc='')
SIG_CREDENTIALS_GH_AUTH_STATUS = signal('SigGHCredentialsAuthStatus', doc='')
