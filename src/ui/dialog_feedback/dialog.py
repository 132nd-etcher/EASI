# coding=utf-8

from src.cfg import Config
from src.qt import QDialog, Qt, QIcon, qt_resources, QDialogButtonBox
from src.newsig.sigmsg import SigMsg
from src.ui.skeletons.dialog_feedback import Ui_Dialog
from src.sentry import crash_reporter


class FeedbackDialog(Ui_Dialog, QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent, flags=Qt.WindowSystemMenuHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        self.setupUi(self)
        self.setWindowIcon(QIcon(qt_resources.app_ico))
        self.setWindowTitle('Your opinion matters')
        self.btn_ok = self.buttonBox.button(QDialogButtonBox.Ok)
        self.btn_cancel = self.buttonBox.button(QDialogButtonBox.Cancel)
        self.btn_ok.setText('Send')
        if Config().usr_name:
            self.nameLineEdit.setText(Config().usr_name)
        if Config().usr_email:
            self.emailLineEdit.setText(Config().usr_email)
        self.btn_ok.clicked.connect(self.btn_ok_clicked)
        self.btn_cancel.clicked.connect(self.btn_cancel_clicked)

    def btn_ok_clicked(self):
        self.accept()

    def btn_cancel_clicked(self):
        self.reject()

    def accept(self):
        mail = self.emailLineEdit.text()
        if mail:
            Config().usr_email = mail
        name = self.nameLineEdit.text()
        if name:
            Config().usr_name = name
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
        SigMsg().show('Thank you', 'Thank you for your feedback !')
        super(FeedbackDialog, self).accept()

    @staticmethod
    def make(parent=None):
        dialog = FeedbackDialog(parent)
        dialog.exec()
