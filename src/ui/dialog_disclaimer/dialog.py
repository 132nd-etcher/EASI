# coding=utf-8

from src.cfg import config
from src.qt import *
from src.ui.skeletons.dialog_disclaimer import Ui_Dialog
from .disclaimer import disclaimers, disclaimers_mod_author


class DisclaimerDialog(Ui_Dialog, QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent, flags=Qt.WindowSystemMenuHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        Ui_Dialog.__init__(self)
        self.setupUi(self)
        self.setWindowIcon(QIcon(qt_resources.app_ico))
        self.setWindowTitle('Important, please read carefully')
        self.buttonBox.button(QDialogButtonBox.Ok).setText('Accept')
        self.buttonBox.button(QDialogButtonBox.Cancel).setText('Decline')

    @staticmethod
    def _make(list_of_disclaimers, special: str = None):
        discs = []
        ks = set()
        for k, t in list_of_disclaimers:
            if k not in config.ack:
                discs.append(t)
                ks.add(k)
        if discs:
            discs.insert(0,
                         '<blockquote><p>By clicking "Accept" below, you explicitly state that you have acknowledged and that you agree with everything on this page.</p></blockquote>')
            dialog = DisclaimerDialog()
            if special:
                dialog.setWindowTitle('{} - {}'.format(dialog.windowTitle(), special))
            dialog.textBrowser.setHtml('<hr />'.join([x for x in discs]))
            if dialog.exec() == 1:
                ack = config.ack
                for k in ks:
                    ack.add(k)
                config.ack = ack
                return True
            else:
                return False
        else:
            return True

    @staticmethod
    def make():
        return DisclaimerDialog._make(disclaimers)

    @staticmethod
    def make_for_mod_authors():
        return DisclaimerDialog._make(disclaimers_mod_author, 'for mod authors only')
