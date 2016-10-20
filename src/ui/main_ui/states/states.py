# coding=utf-8
from src.abstract.ui.main_ui_state import AbstractMainUiState
from src.low.custom_logging import make_logger
from src.sig import sig_main_ui_states
from .state_running import UiStateRunning
from .state_startup import UiStateStartup

logger = make_logger(__name__)


def state_method(func):
    def _wrapper(self, *args, **kwargs):
        try:
            return getattr(self.current_state, func.__name__)(self, *args, **kwargs)
        except AttributeError:
            raise AttributeError('unknown function in MainUiStates: {}'.format(func.__name__))
        except TypeError:
            raise TypeError('incorrect call of {}: ({}) {{{}}}'.format(func.__name__, args, kwargs))

    return _wrapper


class MainUiStateManager(AbstractMainUiState):

    state_mapping = {
        'starting': UiStateStartup,
        'running': UiStateRunning,
    }

    def __init__(self, main_ui_obj_name, main_ui):
        from src.sig import SignalReceiver, CustomSignal
        if not isinstance(sig_main_ui_states, CustomSignal):
            raise TypeError('expected CustomSignal, got: {}'.format(type(sig_main_ui_states)))
        self.main_ui_obj_name = main_ui_obj_name
        self.receiver = SignalReceiver(self)
        self.receiver[sig_main_ui_states] = self.on_sig
        self.current_state = UiStateStartup
        self.main_ui = main_ui

    def on_sig(self, op: str, *args, **kwargs):
        if not hasattr(self.main_ui, self.main_ui_obj_name):
            raise AttributeError('main_ui has not attribute "{}"'.format(self.main_ui_obj_name))
        if not hasattr(self, op):
            raise AttributeError('unknown method for {} class: {}'.format(self.__class__.__name__, op))
        self.main_ui.sig_proc.do(self.main_ui_obj_name, op, *args, **kwargs)

    def set_current_state(self, state: str):
        if not isinstance(state, str):
            raise TypeError('expected a string, got: {}'.format(type(state)))
        if state not in self.state_mapping.keys():
            raise ValueError('unknown state: {}'.format(state))
        self.current_state = self.state_mapping[state]

    @state_method
    def set_progress(self, value: int):
        """"""

    @state_method
    def add_progress(self, value: int):
        """"""

    @state_method
    def set_progress_title(self, value: str):
        """"""

    @state_method
    def set_progress_text(self, value: str):
        """"""

    @state_method
    def show_msg(self, title: str, text: str, over_splash: bool = False):
        """"""
