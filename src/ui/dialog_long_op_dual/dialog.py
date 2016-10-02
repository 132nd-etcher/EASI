# coding=utf-8

from src.abstract.abstract_progress import DualProgressInterface
from src.abstract.ui.connected_dialog import AbstractConnectedDialog
from src.abstract.ui.progress_dialog import BaseProgressDialog
from src.low.custom_logging import make_logger
from src.sig import sig_long_op_dual_dialog
from src.ui.skeletons.dialog_long_op_dual import Ui_Dialog

logger = make_logger(__name__)


class _LongOpDialogDual(Ui_Dialog, BaseProgressDialog):
    def __init__(self, parent=None):
        BaseProgressDialog.__init__(self, parent)

    def set_text(self, value: str):
        self.label.setText(value)


class LongOpDualDialog(AbstractConnectedDialog, DualProgressInterface):
    """Creates the LongOp dialog and transforms Blinker sig to QtSignals via the MainUi Interface"""

    def __init__(self, parent, main_ui_obj_name):
        AbstractConnectedDialog.__init__(self, sig_long_op_dual_dialog, main_ui_obj_name, _LongOpDialogDual(parent))

    def set_progress(self, value: int):
        self.qobj.progress_bar_total.setValue(value)

    def add_progress(self, value: int):
        current = self.qobj.progress_bar_total.value()
        self.qobj.progress_bar_total.setValue(current + value)

    def set_current_progress(self, value: int):
        self.qobj.progressBar.setValue(value)

    def add_current_progress(self, value: int):
        current = self.qobj.progressBar.value()
        self.qobj.progressBar.setValue(current + value)

    def set_current_text(self, value: str):
        self.qobj.label_current.setText(str(value))
        self.adjust_size()

    def set_text(self, value: str):
        self.qobj.label.setText(str(value))
        self.adjust_size()
