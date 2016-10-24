# coding=utf-8

from queue import Queue

from blinker_herald import signals, emit, SENDER_CLASS_NAME

from src.low import constants
from src.qt import QMainWindow, Qt, QIcon, qt_resources
from src.ui.active_dcs_installation import MainUiActiveDCSInstallation
from src.ui.dialog_config.dialog import ConfigDialog
from src.ui.dialog_feedback.dialog import FeedbackDialog
from src.ui.dialog_msg.dialog import MsgDialog
from src.ui.dialog_progress.dialog import ProgressDialog
from src.ui.dialog_testing.dialog import TestingDialog
from src.ui.mod_author import MainUiModAuthor
from src.ui.skeletons.main import Ui_MainWindow
from src.ui.splash.dialog import MainUiSplash
from src.ui.threading import MainGuiThreading
from src.ui.widget_balloon.widget import WidgetBalloon


class MainUi(Ui_MainWindow, QMainWindow, MainGuiThreading):
    threading_queue = Queue()

    def __init__(self):
        # Fucking QMainWindow calls a general super().__init__ on every parent class, don't call them here !
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowCloseButtonHint
        QMainWindow.__init__(
            self,
            parent=None,
            flags=flags | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)

        constants.MAIN_UI = self

        self.testing_dialog = TestingDialog(self)
        self.splash = MainUiSplash(self)
        self.long_op = ProgressDialog(self)
        self.msgbox = MsgDialog(self)
        self.config_dialog = ConfigDialog(self)
        self.active_dcs_installation = MainUiActiveDCSInstallation(self)
        self.mod_author_watcher = MainUiModAuthor(self)
        self.setup()
        self.connect_actions()
        self.setup_children_dialogs()

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

    @emit(sender=SENDER_CLASS_NAME)
    def show(self):
        self.setWindowState(self.windowState() & Qt.WindowMinimized | Qt.WindowActive)
        self.activateWindow()
        super(MainUi, self).show()
        self.raise_()

    def exit(self, code=0):
        self.close()
        if constants.QT_APP:
            constants.QT_APP.exit(code)

    def test_balloon(self):
        from src.qt.palette import PaletteBalloonFive
        palette = PaletteBalloonFive
        WidgetBalloon(self.tableView, 'some info', palette.info, 'topLeft', adjust_size=True)
        WidgetBalloon(self.tableView, 'some warning', palette.warning, 'center', offset_y=-80)
        WidgetBalloon(self.tableView, 'some error', palette.error, 'center', offset_y=-40)
        WidgetBalloon(self.tableView, 'some background', palette.background, 'center')
        WidgetBalloon(self.tableView, 'some note', palette.note, 'center', offset_y=40)


# noinspection PyUnusedLocal
@signals.post_show.connect_via('MainUi')
def test_balloon(sender, signal_emitter, result):
    MainUi.do(None, 'test_balloon')
