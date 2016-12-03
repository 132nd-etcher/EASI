# coding=utf-8

import os

from hypothesis import strategies as st, given, example

from src.sig.sigmsg import SigMsg
from src.ui.dialog_msg.msg_dialog import MsgDialog


@given(text=st.text(), title=st.text())
@example(title='', text='\n')
def test_show(qtbot, mock_main_ui, title, text):
    from src.easi import gui_mode
    gui_mode.post_init_modules()
    dialog = MsgDialog(None)
    qtbot.add_widget(dialog.qobj)
    SigMsg().show(title, text)
    mock_main_ui.do.assert_called_with('msgbox', 'show', args=(title, text))
    dialog.show(title, text)
    assert dialog.qobj.windowTitle() == title
    assert dialog.qobj.label.text() == text.replace('\n', '<br>')


# noinspection PyUnusedLocal
def test_adjust_size(qtbot, mock_main_ui):
    from src.easi import gui_mode
    gui_mode.post_init_modules()
    assert hasattr(mock_main_ui, 'some_obj')
    dialog = MsgDialog(None)
    qtbot.add_widget(dialog.qobj)
    for i in range(1, 40):
        text = '\n'.join(['some text'] * i)
        dialog.show('title', text)
        if os.environ.get('APPVEYOR'):
            assert dialog.qobj.height() >= min((i * 13) + 61, 512)
        else:
            assert dialog.qobj.height() >= (i * 13) + 61, 512
