# coding=utf-8

from src.cfg import config
from src.qt import *
from src.ui.dialog_msg.dialog import MsgDialog
from src.ui.skeletons.dialog_feedback import Ui_Dialog


class _FeedbackDialog(Ui_Dialog, QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent, flags=Qt.WindowSystemMenuHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        self.setupUi(self)
        self.setWindowIcon(QIcon(qt_resources.app_ico))
        self.setWindowTitle('Your opinion matters')
        self.buttonBox.button(QDialogButtonBox.Ok).setText('Send')


class FeedbackDialog:
    def __init__(self, parent=None):
        self.dialog = _FeedbackDialog(parent)

    @staticmethod
    def make(parent=None):
        from src.sentry import crash_reporter
        dialog = FeedbackDialog(parent)
        if config.usr_name:
            dialog.dialog.nameLineEdit.setText(config.usr_name)
        if config.usr_email:
            dialog.dialog.emailLineEdit.setText(config.usr_email)
        if dialog.dialog.exec():
            mail = dialog.dialog.emailLineEdit.text()
            if mail:
                config.usr_email = mail
            name = dialog.dialog.nameLineEdit.text()
            if name:
                config.usr_name = name
            text = dialog.dialog.textEdit.toPlainText()
            crash_reporter.extra_context(
                data={
                    'user': name,
                    'mail': mail,
                }
            )
            type_of_msg = dialog.dialog.comboBox.currentText()
            text = '{}\n{}'.format(type_of_msg, text)
            crash_reporter.captureMessage(
                message=text, level='debug',
                tags={
                    'message': type_of_msg,
                    'type'   : 'message',
                }
            )
            crash_reporter.context.clear()
            MsgDialog.make('Thank you for your feedback !', 'Thank you')
