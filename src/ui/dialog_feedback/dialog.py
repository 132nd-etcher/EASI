# coding=utf-8

from src.cfg import config
from src.qt import QDialog, Qt, QIcon, qt_resources, QDialogButtonBox
from src.sig import sig_msgbox
from src.ui.skeletons.dialog_feedback import Ui_Dialog


class _FeedbackDialog(Ui_Dialog, QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent, flags=Qt.WindowSystemMenuHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        self.setupUi(self)
        self.setWindowIcon(QIcon(qt_resources.app_ico))
        self.setWindowTitle('Your opinion matters')
        self.buttonBox.button(QDialogButtonBox.Ok).setText('Send')
        if config.usr_name:
            self.nameLineEdit.setText(config.usr_name)
        if config.usr_email:
            self.emailLineEdit.setText(config.usr_email)

    def accept(self):
        from src.sentry import crash_reporter
        mail = self.emailLineEdit.text()
        if mail:
            config.usr_email = mail
        name = self.nameLineEdit.text()
        if name:
            config.usr_name = name
        text = self.textEdit.toPlainText()
        crash_reporter.extra_context(
            data={
                'user': name,
                'mail': mail,
            }
        )
        type_of_msg = self.comboBox.currentText()
        text = '{}\n{}'.format(type_of_msg, text)
        crash_reporter.captureMessage(
            message=text, level='debug',
            tags={
                'message': type_of_msg,
                'type': 'message',
            }
        )
        sig_msgbox.show('Thank you', 'Thank you for your feedback !')
        super(_FeedbackDialog, self).accept()


class FeedbackDialog:
    def __init__(self, parent=None):
        self.dialog = _FeedbackDialog(parent)

    @staticmethod
    def make(parent=None):
        dialog = FeedbackDialog(parent)
        dialog.dialog.exec()
