# coding=utf-8


from shortuuid import uuid
import os
from src.cache.cache import Cache
from src.git.own_mod_repo import OwnModRepo
from src.low import constants
from src.low.custom_logging import make_logger
from src.mod.mod_objects.mod_draft import ModDraft
from src.ui.dialog_confirm.dialog import ConfirmDialog
from src.ui.dialog_gh_login.dialog import GHLoginDialog
from src.ui.dialog_msg.dialog import MsgDialog
from src.ui.dialog_new_mod.dialog import NewModDialog

logger = make_logger(__name__)


def gh_account_is_valid(_) -> bool:
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


def collect_basic_meta_data(mod_draft: ModDraft) -> bool:
    return NewModDialog.make(mod_draft, constants.MAIN_UI)


def create_draft_repository(mod_draft: ModDraft) -> bool:
    return isinstance(mod_draft.repo, OwnModRepo)


def add_content(mod_draft: ModDraft) -> bool:
    logger.debug('showing box')
    msg = MsgDialog()
    msg.show('Success', 'Your mod has been created!\n\n'
                        'I\'m going to open it for you, so you may begin adding content to it.\n\n'
                        'WARNING: there is a ".git" folder within you mod folder; do not touch it unless you know '
                        'what you\'re doing ! =)')
    msg.qobj.exec()
    os.startfile(mod_draft.repo.path)
    return True


def func3(mod_draft) -> bool:
    return True


def finalize(mod_draft):
    logger.debug('finalized')


def create_new_mod(resume_uuid=None):
    new_mod_process = [
        gh_account_is_valid,
        collect_basic_meta_data,
        create_draft_repository,
        add_content,
    ]
    if resume_uuid is None:
        mod_draft = ModDraft(uuid=uuid())
    else:
        mod_draft = ModDraft(uuid=resume_uuid)
    while True:
        try:
            func = new_mod_process.pop(0)
            op_name = func.__name__
            op_result = func(mod_draft)
            logger.debug('{}: {}'.format(op_name, op_result))
            if not op_result:
                break
        except IndexError:
            finalize(mod_draft)
            break
    logger.debug('outta the loop')


if __name__ == '__main__':
    Cache('./cache')
    # from src.mod.local_mod import LocalMod
    # logger.debug(LocalMod.drafts())
    # exit(0)
    from src.qt import QApplication
    from src.keyring.keyring import Keyring
    from src.rem.gh.gh_session import GHSession
    import sys

    qt_app = QApplication([])
    GHSession(Keyring().gh_token)
    create_new_mod('TyYH3y9VtEEaK6RNToXgRZ')
    # create_new_mod()
    sys.exit(qt_app.exec())
    sys.exit(0)
    exit(0)
    from src.keyring.keyring import Keyring

    GHSession(Keyring().gh_token)
    create_new_mod()
