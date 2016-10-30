# coding=utf-8


import os

from shortuuid import uuid

from src.git.own_mod_repo import OwnModRepo
from src.low import constants
from src.low.custom_logging import make_logger
from src.mod.mod_objects.mod_draft import ModDraft
from src.rem.gh.gh_session import GHSession
from src.ui.dialog_confirm.dialog import ConfirmDialog
from src.ui.dialog_edit_mod.dialog import NewModDialog
from src.ui.dialog_gh_login.dialog import GHLoginDialog
from src.ui.dialog_mod_files.dialog import ModFilesDialog
from src.ui.dialog_msg.dialog import MsgDialog

logger = make_logger(__name__)


# noinspection PyUnusedLocal
def gh_account_is_valid(*_) -> bool:
    if not GHSession().has_valid_token:
        if ConfirmDialog.make('Creating a mod requires a valid Github account.<br><br>'
                              'Would you like to connect your Github account now?',
                              'Github account not connected'):
            dialog_return = GHLoginDialog.make(constants.MAIN_UI)
            logger.debug(dialog_return)
            return dialog_return
        else:
            return False
    return True


def collect_basic_meta_data(mod_draft: ModDraft, parent_qobj) -> bool:
    return NewModDialog.make(mod_draft, parent_qobj)


def create_draft_repository(mod_draft: ModDraft, _) -> bool:
    return isinstance(mod_draft.repo, OwnModRepo)


def add_content(mod_draft: ModDraft, parent_qobj) -> bool:
    logger.debug('showing box')
    msg = MsgDialog()
    msg.show('Success', 'Your mod has been created!\n\n'
                        'I\'m going to open it for you, so you may begin adding content to it.\n\n'
                        'WARNING: there is a ".git" folder within you mod folder; do not touch it unless you know '
                        'what you\'re doing ! =)')
    msg.qobj.exec()
    os.startfile(mod_draft.repo.path)
    dialog = ModFilesDialog(mod_draft, parent_qobj).qobj
    return dialog.exec() == dialog.Accepted


def finalize(*_):
    logger.debug('finalized')


def create_new_mod(parent_qobj=constants.MAIN_UI):
    new_mod_process = [
        gh_account_is_valid,
        collect_basic_meta_data,
        create_draft_repository,
        add_content,
    ]
    mod_draft = ModDraft(uuid=uuid())
    while True:
        try:
            func = new_mod_process.pop(0)
            op_name = func.__name__
            op_result = func(mod_draft, parent_qobj)
            logger.debug('{}: {}'.format(op_name, op_result))
            if not op_result:
                break
        except IndexError:
            finalize(mod_draft)
            break
    logger.debug('outta the loop')


# if __name__ == '__main__':
#     Cache('./cache')
#     # from src.mod.local_mod import LocalMod
#     # logger.debug(LocalMod.drafts())
#     # exit(0)
#     from src.qt import QApplication
#     from src.keyring.keyring import Keyring
#     from src.rem.gh.gh_session import GHSession
#     from src.dcs.dcs_installs import DCSInstalls
#     import sys
#
#     qt_app = QApplication([])
#     DCSInstalls().discover_dcs_installation()
#     GHSession(Keyring().gh_token)
#     create_new_mod('TyYH3y9VtEEaK6RNToXgRZ')
#     # create_new_mod()
#     sys.exit(qt_app.exec())
#     sys.exit(0)
#     exit(0)
#     from src.keyring.keyring import Keyring
#
#     GHSession(Keyring().gh_token)
#     create_new_mod()
