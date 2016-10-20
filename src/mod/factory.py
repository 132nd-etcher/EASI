# coding=utf-8

import semver
import shortuuid

from src.__version__ import __version__
from src.keyring.keyring import keyring
# from src.ui.dialog_msg.dialog import MsgDialog
from .mod_draft import ModDraft


class ModFactory:
    @staticmethod
    def make_draft():
        gh_account = keyring.gh_username
        if not gh_account:
            # msg = 'Before you can create and share a mod, you will need a Github account linked with EASI.\n\n' \
            #       'To do so, go to the settings page (CTRL+S), and select the "Credentials" tab.'
            # MsgDialog.make(text=msg, title='Oops')
            return None
        mod_draft = ModDraft()
        mod_draft.meta.identifier = shortuuid.uuid()
        mod_draft.meta.meta_version = semver.parse(__version__)['build']
        mod_draft.meta.author = gh_account
        return mod_draft
