# coding=utf-8

from blinker import Signal
from blinker_herald import signals

from src.low import constants
from src.newsig import SIG_PROGRESS, SIG_MSG


def redirect_signal(signal, main_ui_attribute, disconnect_all_others=False):
    assert isinstance(signal, Signal)
    if disconnect_all_others:
        for receiver in [signal.receivers[k] for k in signal.receivers]:
            signal.disconnect(receiver)

    def signal_processor(sender, op, *args, **kwargs):
        if not hasattr(constants.MAIN_UI, main_ui_attribute):
            raise ValueError('MainUi has no attribute "{}"'.format(main_ui_attribute))
        constants.MAIN_UI.do(main_ui_attribute, op, *args, **kwargs)

    signal.connect(signal_processor, weak=False)



# noinspection PyUnusedLocal
def pre_init_modules(*args, **kwargs):
    constants.MAIN_UI.do('splash', 'show')
    redirect_signal(SIG_PROGRESS, 'splash')


# noinspection PyUnusedLocal
def post_discover_dcs_installation(sender, signal_emitter, result):
    constants.MAIN_UI.do('active_dcs_installation', 'known_dcs_installs_changed')


# noinspection PyUnusedLocal
def post_init_modules(*args, **kwargs):
    constants.MAIN_UI.do('splash', 'hide')
    constants.MAIN_UI.do(None, 'show')
    redirect_signal(SIG_PROGRESS, 'long_op', disconnect_all_others=True)
    redirect_signal(SIG_MSG, 'msgbox', disconnect_all_others=True)


def connect_signals():
    signals.pre_init_modules.connect(pre_init_modules)
    signals.post_init_modules.connect(post_init_modules)
    signals.post_discover_dcs_installation.connect(post_discover_dcs_installation)
