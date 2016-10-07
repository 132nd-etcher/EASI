# coding=utf-8
from .base_custom_signal import CustomSignal
from .base_receiver import SignalReceiver
from .interface import interfaced_method, InterfacedSignal
from .sig_author_mode import AuthorModeSig
from .sig_rem import RemSig
from .sig_ui_splash import SplashSig
from .sig_ui_main import MainUiSig, MainUiStatesSig
from .sig_ui_long_op import LongOpDialogSig
from .sig_msgbox import MsgboxSig

sig_dcs_installs_changed = CustomSignal()
sig_sg_path_changed = CustomSignal()
sig_cache_path_changed = CustomSignal()
sig_main_ui_states = MainUiStatesSig()
sig_main_ui = MainUiSig()
sig_author_mode = AuthorModeSig()
sig_long_op_dialog = LongOpDialogSig()
sig_splash = SplashSig()
sig_gh_token_status_changed = RemSig()
sig_db_token_status_changed = RemSig()
sig_interrupt_startup = CustomSignal()
sig_config_changed = CustomSignal()
sig_kdiff_path_changed = CustomSignal()
sig_msgbox = MsgboxSig()


