# coding=utf-8

from unittest import mock
from hypothesis import given, example
from hypothesis import strategies as st

from tests.init_qt_app import QtTestCase


class TestMain(QtTestCase):
    def test_import(self):
        # noinspection PyUnresolvedReferences
        import src.ui.main_ui.states

    def test_run(self):
        from src.sig import sig_main_ui_states
        # from src import main
        # qt_app, main_ui = main.main(test_run=True, init_only=True)
        from src.ui.main_ui.main_ui_threading import MainGuiThreading
        from src.ui.main_ui.states import UiStateStartup
        from src.ui.main_ui.main_ui import MainUi
        self.assertIsInstance(self.main_ui, MainUi)
        self.assertIs(self.main_ui.state_manager.current_state, UiStateStartup)
        # main_ui.state_manager.set_current_state('running')
        m = mock.MagicMock()
        MainGuiThreading.do = m
        sig_main_ui_states.set_current_state('running')
        m.assert_has_calls([mock.call('state_manager', 'set_current_state', args=('running',))])
        sig_main_ui_states.set_current_state('startup')
        m.assert_has_calls(
            [
                mock.call('state_manager', 'set_current_state', args=('running',)),
                mock.call('state_manager', 'set_current_state', args=('startup',))
            ],
        )

    @given(s=st.one_of(st.booleans(), st.integers(), st.floats()))
    def test_wrong_state_type(self, s):
        with self.assertRaises(TypeError):
            self.main_ui.state_manager.set_current_state(s)

    @given(s=st.text())
    def test_wrong_state_name(self, s):
        with self.assertRaises(ValueError):
            self.main_ui.state_manager.set_current_state(s)
