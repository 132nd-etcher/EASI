# coding=utf-8
from .base_custom_signal import CustomSignal
from .base_receiver import SignalReceiver
from .interface import interfaced_method, InterfacedSignal
from .sig_rem import RemSig
from .sig_ui_splash import SplashSig
from .sig_ui_main import MainUiSig, MainUiStatesSig
from .sig_ui_long_op import LongOpDialogSig
from .sig_msgbox import MsgboxSig
from .sig_config_value import ConfigValueSig

sig_cfg_active_dcs_install = ConfigValueSig()
sig_cfg_sg_path = ConfigValueSig()
sig_cfg_cache_path = ConfigValueSig()
sig_cfg_keyring_encrypt = ConfigValueSig()
sig_cfg_kdiff_path = ConfigValueSig()
sig_cfg_author_mode = ConfigValueSig()
sig_cfg_user_name = ConfigValueSig()
sig_cfg_user_mail = ConfigValueSig()
sig_cfg_subscribe_to_test_versions = ConfigValueSig()

sig_main_ui_states = MainUiStatesSig()
sig_main_ui = MainUiSig()
sig_long_op_dialog = LongOpDialogSig()
sig_splash = SplashSig()
sig_gh_token_status_changed = RemSig()
sig_db_token_status_changed = RemSig()
sig_interrupt_startup = CustomSignal()
sig_config_changed = CustomSignal()  # used to update status of config dialog (apply button, ...)
sig_msgbox = MsgboxSig()
sig_known_dcs_installs_changed = CustomSignal()


