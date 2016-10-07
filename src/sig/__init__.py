# coding=utf-8
from .base_custom_signal import CustomSignal
from .base_receiver import SignalReceiver
from .interface import interfaced_method, InterfacedSignal
from .sigs import AbstractLongOpDialogSig, AuthorModeSig, MainUiSig, SplashSig, MainUiStatesSig, RemSig

sig_dcs_installs_changed = CustomSignal()
sig_sg_path_changed = CustomSignal()
sig_cache_path_changed = CustomSignal()
sig_main_ui_states = MainUiStatesSig()
sig_main_ui = MainUiSig()
sig_author_mode = AuthorModeSig()
sig_long_op_dialog = AbstractLongOpDialogSig()
sig_splash = SplashSig()
sig_gh_token_status_changed = RemSig()
sig_db_token_status_changed = RemSig()
sig_interrupt_startup = CustomSignal()
sig_config_changed = CustomSignal()


