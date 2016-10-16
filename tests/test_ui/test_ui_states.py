# coding=utf-8
import pytest
from hypothesis import given
from hypothesis import strategies as st


@given(s=st.one_of(st.booleans(), st.integers(), st.floats()))
def test_wrong_state_type(main_ui, s):
    with pytest.raises(TypeError):
        main_ui.state_manager.set_current_state(s)


@given(s=st.text())
def test_wrong_state_name(main_ui, s):
    with pytest.raises(ValueError):
        main_ui.state_manager.set_current_state(s)
