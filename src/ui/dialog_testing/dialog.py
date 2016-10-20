# coding=utf-8
import time
from src.qt import QDialog, Qt
from src.ui.base.qdialog import BaseDialog
from src.ui.skeletons.dialog_testing import Ui_Dialog
from src.sig import sig_msgbox, sig_progress
from src.threadpool import ThreadPool


from .interface import TestingDialogInterface
from .signal import sig_testing_dialog


class _TestingDialog(Ui_Dialog, QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent, flags=Qt.WindowSystemMenuHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        Ui_Dialog.__init__(self)
        self.setupUi(self)


class TestingDialog(BaseDialog, TestingDialogInterface):
    def __init__(self, parent, main_ui_obj):
        BaseDialog.__init__(self, sig_testing_dialog, main_ui_obj, _TestingDialog(parent))
        self.qobj.btn_make_msgbox.clicked.connect(self.test_msg_box)
        self.qobj.btn_make_progress.clicked.connect(self.test_progress)
        self.qobj.btn_make_dual_progress.clicked.connect(self.test_dual_progress)
        self.pool = ThreadPool(1, 'gui_testing_dialog', True)


    def test_msg_box(self):
        sig_msgbox.show('title', 'text')

    def test_progress(self):
        sig_progress.show('title', 'text')
        self.pool.queue_task(sig_progress.set_progress, [20])
        self.pool.queue_task(time.sleep, [0.5])
        self.pool.queue_task(sig_progress.set_progress, [40])
        self.pool.queue_task(time.sleep, [0.5])
        self.pool.queue_task(sig_progress.set_progress, [60])
        self.pool.queue_task(time.sleep, [0.5])
        self.pool.queue_task(sig_progress.set_progress, [80])
        self.pool.queue_task(time.sleep, [0.5])
        self.pool.queue_task(sig_progress.set_progress, [100])

    def test_dual_progress(self):
        def run_test():
            sig_progress.show('title', 'text')
            sig_progress.set_current_enabled(True)
            sig_progress.set_current_text('first item')
            sig_progress.set_progress(25)
            sig_progress.set_current_progress(50)
            time.sleep(0.5)
            sig_progress.set_progress(50)
            sig_progress.set_current_progress(100)
            time.sleep(0.5)
            sig_progress.set_current_text('second item')
            sig_progress.set_progress(75)
            sig_progress.set_current_progress(50)
            time.sleep(0.5)
            sig_progress.set_progress(75)
            sig_progress.set_current_progress(100)
            sig_progress.set_progress(100)
        self.pool.queue_task(run_test)

    @property
    def qobj(self) -> _TestingDialog:
        return super(TestingDialog, self).qobj

    def show(self):
        self.qobj.show()
