# coding=utf-8

from blinker import Signal
from blinker_herald import signals

from src.low import constants
from src.sig import SIG_PROGRESS, SIG_MSG
from src.easi import ops


def redirect_signal(signal, main_ui_attribute, disconnect_all_others=False):
    assert isinstance(signal, Signal)
    if disconnect_all_others:
        for receiver in [signal.receivers[k] for k in signal.receivers]:
            signal.disconnect(receiver)

    def signal_processor(_, op, *args, **kwargs):
        if not hasattr(constants.MAIN_UI, main_ui_attribute):
            raise ValueError('MainUi has no attribute "{}"'.format(main_ui_attribute))
        constants.MAIN_UI.do(main_ui_attribute, op, *args, **kwargs)

    signal.connect(signal_processor, weak=False)


# noinspection PyUnusedLocal
def pre_init_modules(*args, **kwargs):
    constants.MAIN_UI.do('splash', 'show')
    redirect_signal(SIG_PROGRESS, 'splash')


# noinspection PyUnusedLocal
def post_init_modules(*args, **kwargs):
    constants.MAIN_UI.do('splash', 'hide')
    constants.MAIN_UI.do(None, 'show')
    redirect_signal(SIG_PROGRESS, 'long_op', disconnect_all_others=True)
    redirect_signal(SIG_MSG, 'msgbox', disconnect_all_others=True)


# noinspection PyUnusedLocal
def post_discover_dcs_installation(sender, signal_emitter, result):
    constants.MAIN_UI.do('active_dcs_installation', 'known_dcs_installs_changed')


def connect_signals():
    signals.pre_init_modules.connect(pre_init_modules)
    signals.post_init_modules.connect(post_init_modules)
    signals.post_discover_dcs_installation.connect(post_discover_dcs_installation)


def init_proxies():
    from src.ui.dialog_confirm.dialog import ConfirmDialog
    from src.ui.dialog_browse.dialog import BrowseDialog
    from src.ui.dialog_warn.dialog_warn import WarningDialog
    ops._confirm_func = ConfirmDialog.make
    ops._warn_func = WarningDialog.make

    from src.ui.dialog_select.dialog import SelectDialog
    ops._select_func = SelectDialog.make
    ops._get_directory = BrowseDialog.get_directory
    ops._save_file = BrowseDialog.save_file
    ops._get_file = BrowseDialog.get_file
    ops._get_existing_file = BrowseDialog.get_existing_file
    ops._get_existing_files = BrowseDialog.get_existing_files
