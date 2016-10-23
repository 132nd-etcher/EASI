# coding=utf-8
from .base_custom_signal import CustomSignal
from .base_receiver import SignalReceiver
from .interface import interfaced_method, InterfacedSignal
from .sig_rem import RemSig
from .sig_ui_splash import SplashSig
from .sig_ui_main import MainUiSig, MainUiStatesSig
from .sig_config_value import ConfigValueSig

sig_cfg_author_mode = ConfigValueSig()

sig_gh_token_status_changed = RemSig()
sig_db_token_status_changed = RemSig()
sig_config_changed = CustomSignal()  # used to update status of config dialog (apply button, ...)


