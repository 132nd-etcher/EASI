# coding=utf-8
import random
import string
from pytestqt.qtbot import QtBot
from hypothesis import strategies as st, given, example, settings
from src.ui.dialog_input.dialog import InputDialog
from src.qt import Qt


@given(title=st.text(), text=st.text(), label1=st.text(), default1=st.text())
@example(title='', text='', label1='', default1='0')
@settings(max_examples=20)
def test_input_dialog_basics(title, text,
                             label1,
                             default1,
                             qtbot: QtBot):
    dialog = InputDialog()
    qtbot.add_widget(dialog)
    dialog.set_title(title)
    dialog.set_text(text)
    assert dialog.windowTitle() == title
    assert dialog.label.text() == text.replace('\n', '<br>')
    dialog.add_question(label1, default1)
    dialog.add_question('label2')
    dialog.show()
    qtbot.wait_for_window_shown(dialog)
    # noinspection PyUnresolvedReferences
    qtbot.mouseClick(dialog.btn_ok, Qt.LeftButton)
    qtbot.wait_signal(dialog.accepted)
    qtbot.wait_until(lambda: dialog.isVisible() is False)
    assert dialog.result[label1] == default1
    assert dialog.result['label2'] == ''


@given(label=st.text(min_size=1), default=st.text(), some_text=st.text(min_size=1, max_size=64))
@settings(max_examples=20)
def test_input_dialog_results(label, default, some_text, qtbot: QtBot):
    dialog = InputDialog()
    qtbot.add_widget(dialog)
    dialog.add_question(label, default)
    random_string = ''.join(random.choice(string.ascii_lowercase) for _ in range(32))
    dialog.questions[label].clear()
    # noinspection PyUnresolvedReferences
    qtbot.keyClicks(dialog.questions[label], random_string)
    assert dialog.questions[label].text() == random_string
    dialog.show()
    qtbot.wait_for_window_shown(dialog)
    # noinspection PyUnresolvedReferences
    qtbot.mouseClick(dialog.btn_ok, Qt.LeftButton)
    qtbot.wait_signal(dialog.accepted)
    qtbot.wait_until(lambda: dialog.isVisible() is False)
    qtbot.wait_until(lambda: dialog.questions[label].text() == random_string)
    assert dialog.result[label] == random_string
    dialog.questions[label].setText(some_text)
    dialog.show()
    qtbot.wait_for_window_shown(dialog)
    # noinspection PyUnresolvedReferences
    qtbot.mouseClick(dialog.btn_ok, Qt.LeftButton)
    qtbot.wait_signal(dialog.accepted)
    qtbot.wait_until(lambda: dialog.isVisible() is False)
    assert dialog.result[label] == some_text
