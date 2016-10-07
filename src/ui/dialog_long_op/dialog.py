# coding=utf-8

from src.abstract.abstract_progress import ProgressInterface
from src.abstract.ui.connected_dialog import AbstractConnectedDialog
from src.abstract.ui.progress_dialog import BaseProgressDialog
from src.low.custom_logging import make_logger
from src.sig import sig_long_op_dialog
from src.ui.skeletons.dialog_long_op import Ui_Dialog

logger = make_logger(__name__)


class _LongOpDialog(Ui_Dialog, BaseProgressDialog):
    def __init__(self, parent=None):
        BaseProgressDialog.__init__(self, parent)


class LongOpDialog(AbstractConnectedDialog, ProgressInterface):
    """Creates the LongOp dialog and transforms Blinker sig to QtSignals via the MainUi Interface"""

    def __init__(self, parent, main_ui_obj_name):
        AbstractConnectedDialog.__init__(self, sig_long_op_dialog, main_ui_obj_name, _LongOpDialog(parent))
        self.set_current_enabled(False)

    # noinspection PyMethodOverriding
    def show(self, title: str, text: str):
        self.dialog.setWindowTitle(title)
        self.dialog.label.setText(text)
        super(LongOpDialog, self).show()


    @property
    def dialog(self) -> _LongOpDialog:
        return self.qobj

    def set_current_enabled(self, value: bool):
        self.dialog.label_current.setVisible(value)
        self.dialog.progressBar.setVisible(value)

    @staticmethod
    def make(*args, **kwargs):
        raise NotImplementedError('use signals')

    def set_progress(self, value: int):
        self.dialog.progress_bar_total.setValue(value)

    def add_progress(self, value: int):
        self.qobj.progress_bar_total.setValue(self.qobj.progressBar.value() + value)

    def set_text(self, value: str):
        self.dialog.label.setText(str(value))
        self.dialog.label.adjustSize()
        self.adjust_size()

    def set_current_progress(self, value: int):
        self.dialog.progressBar.setValue(value)

    def add_current_progress(self, value: int):
        current = self.qobj.progressBar.value()
        self.dialog.progressBar.setValue(current + value)

    def set_current_text(self, value: str):
        self.dialog.label_current.setText(str(value))
        # self.adjust_size()
