# coding=utf-8

from src.qt import QDialog, Qt
from src.ui.base.qdialog import BaseDialog
from src.ui.skeletons.dialog_modmanager import Ui_Dialog


class _ModManager(Ui_Dialog, QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent, flags=Qt.WindowSystemMenuHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        self.setupUi(self)
        self.setWindowTitle('Mod manager')
        self.btn_exit.clicked.connect(self.close)


class ModManagerDialog(BaseDialog):
    def __init__(self, parent=None):
        BaseDialog.__init__(self, _ModManager(parent))


if __name__ == '__main__':
    from src.qt import QApplication
    import sys

    qt_app = QApplication([])
    dialog = ModManagerDialog()
    dialog.qobj.show()
    sys.exit(qt_app.exec())
