# coding=utf-8
import time

from src.newsig.sigmsg import SigMsg
from src.newsig.sigprogress import SigProgress
from src.qt import QDialog, Qt
from src.threadpool import ThreadPool
from src.ui.base.qdialog import BaseDialog
from src.ui.dialog_confirm.dialog import ConfirmDialog
from src.ui.dialog_input.dialog import InputDialog
from src.ui.dialog_testing.interface import TestingDialogInterface
from src.ui.skeletons.dialog_testing import Ui_Dialog
from src.ui.widget_logger.widget import QtLogger


class _TestingDialog(Ui_Dialog, QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent, flags=Qt.WindowSystemMenuHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        Ui_Dialog.__init__(self)
        self.setupUi(self)


class TestingDialog(BaseDialog, TestingDialogInterface):
    def __init__(self, parent):
        BaseDialog.__init__(self, _TestingDialog(parent))
        self.qobj.btn_make_msgbox.clicked.connect(self.test_msg_box)
        self.qobj.btn_make_progress.clicked.connect(self.test_progress)
        self.qobj.btn_make_dual_progress.clicked.connect(self.test_dual_progress)
        self.qobj.btn_make_confirm.clicked.connect(self.test_confirm_dialog)
        self.qobj.btn_make_input_dialog.clicked.connect(self.test_input_dialog)
        self.qobj.btn_test_logger.clicked.connect(self.test_logger)
        self.pool = ThreadPool(1, 'gui_testing_dialog', True)

    def test_msg_box(self):
        SigMsg().show('title', 'text')

    def test_progress(self):
        def run_test():
            progress = SigProgress()
            progress.show('title', 'text')
            progress.set_progress(20)
            time.sleep(0.5)
            progress.set_progress(40)
            time.sleep(0.5)
            progress.set_progress(60)
            time.sleep(0.5)
            progress.set_progress(80)
            time.sleep(0.5)
            progress.set_progress(100)

        self.pool.queue_task(run_test)

    def test_dual_progress(self):
        def run_test():
            progress = SigProgress()
            progress.show('title', 'text')
            progress.set_current_enabled(True)
            progress.set_current_text('first item')
            progress.set_progress(25)
            progress.set_current_progress(50)
            time.sleep(0.5)
            progress.set_progress(50)
            progress.set_current_progress(100)
            time.sleep(0.5)
            progress.set_current_text('second item')
            progress.set_progress(75)
            progress.set_current_progress(50)
            time.sleep(0.5)
            progress.set_progress(75)
            progress.set_current_progress(100)
            progress.set_progress(100)

        self.pool.queue_task(run_test)

    def test_input_dialog(self):
        result = InputDialog.make('test', 'title', [('Value1', 'default1'), ('Value2', '')])
        if result:
            SigMsg().show('Results', '\n'.join(['{}: {}'.format(k, result[k]) for k in result.keys()]))
        else:
            SigMsg().show('Result', 'Operation cancelled')

    def test_confirm_dialog(self):
        result = ConfirmDialog.make('question', 'title')
        SigMsg().show('Result', str(result))

    def test_logger(self):
        self.qobj.textBrowser.insertPlainText('test\n')
        self.qobj.textBrowser.insertPlainText('test\n')
        self.qobj.textBrowser.insertPlainText('test\n')
        self.qobj.textBrowser.insertPlainText('test\n')
        self.qobj.textBrowser.insertPlainText('test\n')
        self.qobj.textBrowser.insertPlainText('test\n')

    @property
    def qobj(self) -> _TestingDialog:
        return super(TestingDialog, self).qobj

    def show(self):
        self.qobj.show()
