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

    def set_progress(self, value: int):
        self.qobj.progressBar.setValue(value)

    def add_progress(self, value: int):
        self.qobj.progressBar.setValue(self.qobj.progressBar.value() + value)

    def set_text(self, value: str):
        self.qobj.label.setText(str(value))
        self.adjust_size()
