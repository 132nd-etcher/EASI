# coding=utf-8


from src.qt import QWizard, Qt, QApplication
from src.ui.base.qdialog import BaseDialog
from src.ui.skeletons.wizard_newmod import Ui_Wizard
from src.ui.wizard_newmod.page1_mod_name import PageModName


class _NewModWizard(Ui_Wizard, QWizard):
    def __init__(self, parent=None):
        QWizard.__init__(self, parent, flags=Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        self.setupUi(self)
        self.addPage(PageModName('Mod name', self))

    def accept(self):
        print('accepted')
        print(self.field('modname'))
        super(_NewModWizard, self).accept()

    def reject(self):
        print('rejected')
        super(_NewModWizard, self).reject()


class NewModWizard(BaseDialog):
    def __init__(self, parent=None):
        BaseDialog.__init__(self, _NewModWizard(parent))


if __name__ == '__main__':
    qt_app = QApplication([])
    dialog = NewModWizard()
    dialog.qobj.show()
    qt_app.exec()
