# coding=utf-8
import time

from src.qt import QDialog, Qt
from src.sig import sig_msgbox, sig_progress
from src.threadpool import ThreadPool
from src.ui.base.qdialog import BaseDialog
from src.ui.base.with_signal import WithSignal
from src.ui.dialog_input.dialog import InputDialog
from src.ui.dialog_confirm.dialog import ConfirmDialog
from src.ui.skeletons.dialog_testing import Ui_Dialog
from .interface import TestingDialogInterface
from .signal import sig_testing_dialog


class _TestingDialog(Ui_Dialog, QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent, flags=Qt.WindowSystemMenuHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        Ui_Dialog.__init__(self)
        self.setupUi(self)


class TestingDialog(BaseDialog, WithSignal, TestingDialogInterface):
    def __init__(self, parent, main_ui_obj):
        BaseDialog.__init__(self, _TestingDialog(parent))
        WithSignal.__init__(self, sig_testing_dialog, main_ui_obj)
        self.qobj.btn_make_msgbox.clicked.connect(self.test_msg_box)
        self.qobj.btn_make_progress.clicked.connect(self.test_progress)
        self.qobj.btn_make_dual_progress.clicked.connect(self.test_dual_progress)
        self.qobj.btn_make_confirm.clicked.connect(self.test_confirm_dialog)
        self.qobj.btn_make_input_dialog.clicked.connect(self.test_input_dialog)
        self.pool = ThreadPool(1, 'gui_testing_dialog', True)

    def test_msg_box(self):
        sig_msgbox.show('title', 'text')

    def test_progress(self):
        def run_test():
            sig_progress.show('title', 'text')
            sig_progress.set_progress(20)
            time.sleep(0.5)
            sig_progress.set_progress(40)
            time.sleep(0.5)
            sig_progress.set_progress(60)
            time.sleep(0.5)
            sig_progress.set_progress(80)
            time.sleep(0.5)
            sig_progress.set_progress(100)

        self.pool.queue_task(run_test)

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

    def test_input_dialog(self):
        result = InputDialog.make('test', 'title', [('Value1', 'default1'), ('Value2', '')])
        if result:
            sig_msgbox.show('Results', '\n'.join(['{}: {}'.format(k, result[k]) for k in result.keys()]))
        else:
            sig_msgbox.show('Result', 'Operation cancelled')

    def test_confirm_dialog(self):
        result = ConfirmDialog.make('question', 'title')
        sig_msgbox.show('Result', str(result))

    @property
    def qobj(self) -> _TestingDialog:
        return super(TestingDialog, self).qobj

    def show(self):
        self.qobj.show()
