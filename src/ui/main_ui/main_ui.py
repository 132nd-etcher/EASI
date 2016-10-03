# coding=utf-8

from queue import Queue

from src.low import constants
from src.qt import *
from ..dialog_config.dialog import ConfigDialog
from ..dialog_feedback.dialog import FeedbackDialog
from ..dialog_long_op.dialog import LongOpDialog
# noinspection PyPackageRequirements
from .interface.interface import MainUiSigProcessor
from .main_ui_active_dcs_installation import MainUiActiveDCSInstallation
from .main_ui_threading import MainGuiThreading
from .states import MainUiStateManager
from .main_ui_mod_author import MainUiModAuthor
from ..skeletons.main import Ui_MainWindow
from ..splash.dialog import MainUiSplash


# from src.abstract.ui import AbstractConnectedQObject

class MainUi(Ui_MainWindow, QMainWindow, MainGuiThreading):
    threading_queue = Queue()

    def __init__(self, qt_app: QApplication):
        # Fucking QMainWindow calls a general super().__init__ on every parent class, don't call them here !
        QMainWindow.__init__(self,
                             parent=None,
                             flags=Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)

        self.qt_app = qt_app

        # Setup link with all connected objects
        import src.abstract.ui.connected_object
        src.abstract.ui.connected_object.main_ui = self
        self.sig_proc = MainUiSigProcessor(self)
        self.splash = MainUiSplash(self, 'splash')
        self.long_op = LongOpDialog(self, 'long_op')
        self.config_dialog = ConfigDialog(self)
        self.active_dcs_installation = MainUiActiveDCSInstallation(self)
        self.mod_author_watcher = MainUiModAuthor(self)
        self.setup()
        self.connect_actions()
        self.setup_children_dialogs()
        self.state_manager = MainUiStateManager('state_manager')

    def setup(self):
        self.setupUi(self)
        self.setWindowTitle(
            '{} {} v{} - {}'.format(constants.APP_SHORT_NAME,
                                    constants.APP_STATUS,
                                    constants.APP_VERSION,
                                    constants.APP_RELEASE_NAME))
        self.setWindowIcon(QIcon(qt_resources.app_ico))

    def connect_actions(self):
        self.actionExit.triggered.connect(self.exit)
        self.actionEASI_Settings.triggered.connect(self.config_dialog.show)
        self.actionFeedback.triggered.connect(lambda x: FeedbackDialog.make(self))

    def setup_children_dialogs(self):
        self.active_dcs_installation.setup()
        self.config_dialog.setup()
        self.mod_author_watcher.setup()

    def show(self):
        self.setWindowState(self.windowState() & Qt.WindowMinimized | Qt.WindowActive)
        self.activateWindow()
        super(MainUi, self).show()
        self.raise_()

    def exit(self, code=0):
        self.close()
        self.qt_app.exit(code)
