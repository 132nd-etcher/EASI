# coding=utf-8

import random
from unittest import mock

from PyQt5.Qt import QTest
from hypothesis import strategies as st, given, example, settings
from pytestqt.qtbot import QtBot

from src.cfg import Config
from src.qt import Qt
from src.ui.dialog_feedback.dialog import FeedbackDialog


@given(usr_name=st.text(), usr_mail=st.text())
def test_dialog_feedback_field_population(qtbot: QtBot, config, usr_name, usr_mail):
    Config().usr_name = usr_name
    Config().usr_email = usr_mail
    dialog = FeedbackDialog()
    qtbot.add_widget(dialog)
    assert dialog.nameLineEdit.text() == usr_name
    assert dialog.emailLineEdit.text() == usr_mail


@given(some_text=st.text(max_size=200))
@example(some_text='\r\n')
@settings(max_examples=5)
def test_feedback(qtbot: QtBot, mocker, config, some_text):
    assert isinstance(qtbot, (QtBot, QTest))
    msgbox = mocker.patch('src.ui.dialog_feedback.dialog.sig_msgbox.show')
    crash_reporter = mocker.patch('src.ui.dialog_feedback.dialog.crash_reporter', captureMessage=mock.MagicMock())
    dialog = FeedbackDialog()
    qtbot.add_widget(dialog)
    dialog.show()
    qtbot.wait_for_window_shown(dialog)
    dialog.textEdit.setText(some_text)
    dialog.comboBox.setCurrentIndex(random.randint(0, dialog.comboBox.count()))

    qtbot.mouseClick(dialog.btn_ok, Qt.LeftButton)

    crash_reporter.captureMessage.assert_called_with(
        level='debug',
        message='{}\n{}'.format(
            dialog.comboBox.currentText(),
            some_text.replace('\r\n', '\n').replace('\r', '\n').replace('\xa0', ' ')
        ),
        tags={
            'message': dialog.comboBox.currentText(),
            'type': 'message'
        }
    )
    msgbox.assert_called_with('Thank you', 'Thank you for your feedback !')
