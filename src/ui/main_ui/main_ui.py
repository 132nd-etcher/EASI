# coding=utf-8

from queue import Queue

from blinker_herald import signals
from ..widget_balloon.widget import WidgetBalloon

from src.low import constants
from src.qt import QApplication, QMainWindow, Qt, QIcon, qt_resources
from src.ui.main_ui.interface.interface import MainUiSigProcessor
from src.ui.splash.dialog import MainUiSplash
from .main_ui_active_dcs_installation import MainUiActiveDCSInstallation
from .main_ui_mod_author import MainUiModAuthor
from .main_ui_threading import MainGuiThreading
from .states import MainUiStateManager
from ..dialog_config.dialog import ConfigDialog
from ..dialog_feedback.dialog import FeedbackDialog
from ..dialog_msg.dialog import MsgDialog
from ..dialog_progress.dialog import ProgressDialog
from ..dialog_testing.dialog import TestingDialog
from ..skeletons.main import Ui_MainWindow


# from src.abstract.ui import AbstractConnectedQObject

class MainUi(Ui_MainWindow, QMainWindow, MainGuiThreading):
    threading_queue = Queue()

    def __init__(self, qt_app: QApplication or None):
        # Fucking QMainWindow calls a general super().__init__ on every parent class, don't call them here !
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowCloseButtonHint
        QMainWindow.__init__(
            self,
            parent=None,
            flags=flags | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)

        self.qt_app = qt_app

        # # Setup link with all connected objects
        # import src.abstract.ui.connected_object
        # src.abstract.ui.connected_object.main_ui = self

        # Give a heads-up to all child QWidgets that the MainUi is up and running
        import src.ui.base.with_signal
        src.ui.base.with_signal.main_ui = self

        self.sig_proc = MainUiSigProcessor(self)
        self.testing_dialog = TestingDialog(self, 'test_dialog')
        self.splash = MainUiSplash(self, 'splash')
        self.long_op = ProgressDialog(self, 'long_op')
        self.msgbox = MsgDialog(self, 'msgbox')
        self.config_dialog = ConfigDialog(self)
        self.active_dcs_installation = MainUiActiveDCSInstallation(self)
        self.mod_author_watcher = MainUiModAuthor(self)
        self.setup()
        self.connect_actions()
        self.setup_children_dialogs()
        self.state_manager = MainUiStateManager('state_manager', self)

    def setup(self):
        self.setupUi(self)
        self.setWindowTitle(
            '{} v{} - {}'.format(constants.APP_SHORT_NAME,
                                 constants.APP_VERSION,
                                 constants.APP_RELEASE_NAME))
        self.setWindowIcon(QIcon(qt_resources.app_ico))

    def connect_actions(self):
        self.actionExit.triggered.connect(self.exit)
        self.actionEASI_Settings.triggered.connect(self.config_dialog.show)
        self.actionFeedback.triggered.connect(lambda x: FeedbackDialog.make(self))
        self.actionTest_dialog.triggered.connect(self.testing_dialog.show)

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
        if self.qt_app:
            self.qt_app.exit(code)

    def test_balloon(self):
        from src.qt.palette import PaletteBalloonFive
        palette = PaletteBalloonFive
        WidgetBalloon(self.tableView, 'some info', palette.info, 'topLeft', adjust_size=True)
        WidgetBalloon(self.tableView, 'some warning', palette.warning, 'center', offset_y=-80)
        WidgetBalloon(self.tableView, 'some error', palette.error, 'center', offset_y=-40)
        WidgetBalloon(self.tableView, 'some background', palette.background, 'center')
        WidgetBalloon(self.tableView, 'some note', palette.note, 'center', offset_y=40)


# noinspection PyUnusedLocal
@signals.post_init_modules.connect
def test_balloon(sender, signal_emitter, result):
    MainUi.do('splash', 'hide')
    MainUi.do(None, 'show')
    MainUi.do(None, 'test_balloon')
