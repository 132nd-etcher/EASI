# coding=utf-8

from src.qt import QDialog, Qt
from src.abstract.progress_interface import IProgress
from src.low.custom_logging import make_logger
from src.ui.skeletons.dialog_progress import Ui_Dialog
from src.ui.base.qdialog import BaseDialog

logger = make_logger(__name__)


class _ProgressDialog(Ui_Dialog, QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent, Qt.WindowTitleHint)
        self.setupUi(self)
        self.setWindowModality(Qt.ApplicationModal)

    def reject(self):
        pass


class ProgressDialog(BaseDialog, IProgress):
    """Creates the LongOp dialog and transforms Blinker sig to QtSignals via the MainUi Interface"""

    def __init__(self, parent):
        BaseDialog.__init__(self, _ProgressDialog(parent))
        self.set_current_enabled(False)
        self.__auto_close = True
        self.__current_enabled = False

    def show(self, title: str, text: str = '', auto_close=True):
        self.qobj.setWindowTitle(title)
        self.qobj.label.setText(text)
        self.__auto_close = auto_close
        self.qobj.show()

    @property
    def qobj(self) -> _ProgressDialog:
        return super(ProgressDialog, self).qobj

    def set_current_enabled(self, value: bool):
        self.__current_enabled = value
        self.qobj.label_current.setVisible(value)
        self.qobj.progressBar.setVisible(value)

    def set_progress(self, value: int):
        self.qobj.progress_bar_total.setValue(value)
        if value == 100 and self.__auto_close:
            self.hide()

    def hide(self):
        self.qobj.hide()
        self.set_progress(0)
        self.set_current_progress(0)
        self.set_current_enabled(False)

    def add_progress(self, value: int):
        self.qobj.progress_bar_total.setValue(self.qobj.progressBar.value() + value)

    def set_progress_title(self, value: str):
        logger.debug('starting: {}'.format(value))
        self.qobj.setWindowTitle(value)

    def set_progress_text(self, value: str):
        logger.debug('starting: {}'.format(value))
        if not self.qobj.isVisible():
            self.show('Please wait...')
        self.qobj.label.setText(str(value))
        self.qobj.label.adjustSize()
        self.adjust_size()

    def set_current_progress(self, value: int):
        if not self.__current_enabled:
            self.set_current_enabled(True)
        self.qobj.progressBar.setValue(value)

    def add_current_progress(self, value: int):
        if not self.__current_enabled:
            self.set_current_enabled(True)
        current = self.qobj.progressBar.value()
        self.qobj.progressBar.setValue(current + value)

    def set_current_text(self, value: str):
        if not self.__current_enabled:
            self.set_current_enabled(True)
        self.qobj.label_current.setText(str(value))
        # self.adjust_size()
