# coding=utf-8

from queue import Queue

from blinker_herald import emit, SENDER_CLASS_NAME

from src.low import constants
from src.qt import QMainWindow, Qt, QIcon, qt_resources
from src.ui.active_dcs_installation import MainUiActiveDCSInstallation
from src.ui.dialog_config.dialog import ConfigDialog
from src.ui.dialog_feedback.dialog import FeedbackDialog
from src.ui.dialog_msg.dialog import MsgDialog
from src.ui.dialog_progress.dialog import ProgressDialog
from src.ui.dialog_testing.dialog import TestingDialog
from src.ui.form_table_own_mods.form import ModEditor
from src.ui.mod_author import MainUiModAuthor
from src.ui.skeletons.main import Ui_MainWindow
from src.ui.splash.dialog import MainUiSplash
from src.ui.threading import MainGuiThreading
from src.ui.form_table_repositories.form_table_repositories import MetaRepoTable
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
        self.mod_author = MainUiModAuthor(self)  # TODO: remove
        self.feedback_dialog = FeedbackDialog(self)
        # self.meta_repos = MetaRepoTable(self)
        # self.own_mods = ModEditor(self)
        self.repos = MetaRepoTable(self)
        self.editor = ModEditor(self)
        self.setup()
        self.connect_actions()
        self.setup_children_dialogs()
        self.show_widget(self.editor.qobj)
        self.btn_editor.setChecked(True)

    def show_widget(self, widget):
        self.repos.qobj.hide()
        self.editor.qobj.hide()
        widget.show()

    def setup(self):
        self.setupUi(self)
        self.setWindowTitle(
            '{} v{} - {}'.format(constants.APP_SHORT_NAME,
                                 constants.APP_VERSION,
                                 constants.APP_RELEASE_NAME))
        self.setWindowIcon(QIcon(qt_resources.app_ico))
        self.main_layout.addWidget(self.repos.qobj)
        self.main_layout.addWidget(self.editor.qobj)

    def connect_actions(self):
        self.actionExit.triggered.connect(self.exit)
        self.actionEASI_Settings.triggered.connect(self.config_dialog.show)
        self.actionFeedback.triggered.connect(self.feedback_dialog.show)
        self.actionTest_dialog.triggered.connect(self.testing_dialog.show)
        self.btn_editor.clicked.connect(lambda: self.show_widget(self.editor.qobj))
        self.btn_repos.clicked.connect(lambda: self.show_widget(self.repos.qobj))

    def setup_children_dialogs(self):
        self.active_dcs_installation.setup()
        self.config_dialog.setup()
        self.mod_author.setup()

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


# # noinspection PyUnusedLocal
# @signals.post_show.connect_via('MainUi')
# def test_balloon(sender, signal_emitter, result):
#     MainUi.do(None, 'test_balloon')
