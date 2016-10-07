# coding=utf-8

import random
from hypothesis import strategies as st, given, example, settings
from tests.init_qt_app import QtTestCase
from src.ui import FeedbackDialog, MsgDialog
from src.cfg import config
from src.sentry import crash_reporter
from unittest import mock
from PyQt5.QtCore import QTimer


class TestDialogFeedback(QtTestCase):

    @given(usr_name=st.text(), usr_mail=st.text())
    def test_dialog_feedback_field_population(self, usr_name, usr_mail):
        config.usr_name = usr_name
        config.usr_email = usr_mail
        dialog = FeedbackDialog()
        self.assertSequenceEqual(dialog.dialog.nameLineEdit.text(), usr_name)
        self.assertSequenceEqual(dialog.dialog.emailLineEdit.text(), usr_mail)

    @given(some_text=st.text())
    @example(some_text='\r\n')
    @settings(max_examples=20)
    def test_feedback(self, some_text):
        msg = mock.MagicMock()
        MsgDialog.make = msg
        m = mock.MagicMock()
        crash_reporter.captureMessage = m
        dialog = FeedbackDialog()
        dialog.dialog.show()
        dialog.dialog.comboBox.setCurrentIndex(random.randint(0, dialog.dialog.comboBox.count()))
        dialog.dialog.textEdit.setText(some_text)
        QTimer.singleShot(0, dialog.dialog.buttonBox.button(dialog.dialog.buttonBox.Ok).clicked)
        dialog.dialog.exec()
        m.assert_called_with(
            level='debug',
            message='{}\n{}'.format(
                dialog.dialog.comboBox.currentText(),
                some_text.replace('\r\n', '\n').replace('\r', '\n').replace('\xa0', ' ')
            ),
            tags={
                'message': dialog.dialog.comboBox.currentText(),
                'type': 'message'
            }
        )
        msg.assert_called_with('Thank you for your feedback !', 'Thank you')
