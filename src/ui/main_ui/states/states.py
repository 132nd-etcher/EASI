# coding=utf-8

from src.abstract.ui.connected_object import AbstractConnectedObject
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

    return _wrapper


class MainUiStateManager(AbstractConnectedObject, AbstractMainUiState):

    state_mapping = {
        'starting': UiStateStartup,
        'running' : UiStateRunning,
    }

    def __init__(self, main_ui_obj_name):
        AbstractConnectedObject.__init__(self, sig_main_ui_states, main_ui_obj_name)
        self.current_state = UiStateStartup

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
    def set_progress_text(self, value: str):
        """"""
