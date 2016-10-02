# coding=utf-8
from .base_custom_signal import CustomSignal
from .base_receiver import SignalReceiver
from .interface import interfaced_method, InterfacedSignal
from .sigs import *

sig_dcs_installs_changed = CustomSignal()
sig_sg_path_changed = CustomSignal()
sig_cache_path_changed = CustomSignal()
sig_main_ui_states = MainUiStatesSig()
sig_main_ui = MainUiSig()
sig_author_mode = AuthorModeSig()
sig_long_op_dialog = AbstractLongOpDialogSig()
sig_long_op_dual_dialog = AbstractLongOpDualDialogSig()
sig_splash = SplashSig()
