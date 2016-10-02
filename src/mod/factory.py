# coding=utf-8

import shortuuid

from src.__version__ import version
from src.keyring.keyring import keyring
from src.ui.dialog_msg.dialog import MsgDialog
from .mod_draft import ModDraft


class ModFactory:
    @staticmethod
    def make_draft():
        gh_account = keyring.gh_username
        if not gh_account:
            msg = 'Before you can create and share a mod, you will need a Github account linked with EASI.\n\n' \
                  'To do so, go to the settings page (CTRL+S), and select the "Credentials" tab.'
            MsgDialog.make(text=msg, title='Oops')
            return None
        mod_draft = ModDraft()
        mod_draft.meta.identifier = shortuuid.uuid()
        mod_draft.meta.meta_version = version.build
        mod_draft.meta.author = gh_account
        return mod_draft
