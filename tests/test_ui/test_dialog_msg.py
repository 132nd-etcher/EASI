# coding=utf-8

import os

from hypothesis import strategies as st, given, example

from src.sig import sig_msgbox
from src.ui.dialog_msg.dialog import MsgDialog


@given(text=st.text(), title=st.text())
@example(title='', text='\n')
def test_show(qtbot, main_ui, title, text):
    dialog = MsgDialog(None, 'msgbox')
    qtbot.add_widget(dialog.qobj)
    sig_msgbox.show(title, text)
    main_ui.sig_proc.do.assert_called_with('msgbox', 'show', args=(title, text))
    dialog.show(title, text)
    assert dialog.qobj.windowTitle() == title
    assert dialog.qobj.label.text() == text.replace('\n', '<br>')


def test_adjust_size(qtbot, main_ui):
    dialog = MsgDialog(None, 'msgbox')
    qtbot.add_widget(dialog.qobj)
    for i in range(1, 40):
        text = '\n'.join(['some text'] * i)
        dialog.show('title', text)
        if os.environ.get('APPVEYOR'):
            assert dialog.qobj.height() >= min((i * 13) + 61, 512)
        else:
            assert dialog.qobj.height() >= (i * 13) + 61, 512
