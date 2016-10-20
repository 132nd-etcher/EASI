# coding=utf-8

from src.abstract.progress_interface import ProgressInterface
from src.low import constants
from src.qt import QSplashScreen, QPixmap, qt_resources, Qt, QLabel, QFont, QProgressBar
from src.sig import sig_splash
from src.ui.base.qwidget import BaseQWidget
from src.ui.base.with_signal import WithSignal


class _MainUiSplash(QSplashScreen):
    def __init__(self, parent):
        QSplashScreen.__init__(self, parent, QPixmap(qt_resources.splash_banner), Qt.WindowStaysOnTopHint)
        self.colors = {
            'text': '30,30,30,255'
        }
        self.label_version = QLabel('v{}'.format(constants.APP_VERSION), self)
        font = self.label_version.font()
        # font.setBold(True)
        font.setPointSize(14)
        self.label_version.setFixedWidth(200)
        self.label_version.setAlignment(Qt.AlignRight)
        self.label_version.setFont(font)
        # self.label_version.setStyleSheet("color: rgba(255,255,255,255)")
        self.label_version.setStyleSheet("color: rgba({})".format(self.colors['text']))
        self.label_version.setGeometry(
            self.width() - self.label_version.width() - 33,
            self.height() - self.label_version.height() - 45,
            self.label_version.width(),
            self.label_version.height()
        )
        # Harrington
        # Kunstler Script
        # Lucida Handwriting
        # Mistral
        # Monotype Corsiva
        # Palace Script MT
        # Vivaldi
        self.label_rel_name = QLabel('{}'.format(constants.APP_RELEASE_NAME), self)
        h_offset = 40
        # font = QFont('Monotype Corsiva', 20)
        font = QFont('Lucida Handwriting', 16)
        self.label_rel_name.setWordWrap(True)
        self.label_rel_name.setFont(font)
        self.label_rel_name.setFixedWidth(self.width() - h_offset - self.label_version.width())
        self.label_rel_name.setFixedHeight(80)
        # self.label_rel_name.setStyleSheet("color: rgba(255,255,255,255)")
        self.label_rel_name.setStyleSheet("color: rgba({})".format(self.colors['text']))
        self.label_rel_name.setGeometry(
            h_offset,
            100,
            self.label_rel_name.width(),
            self.label_rel_name.height()
        )
        self.progress = QProgressBar(self)
        self.progress.setStyleSheet("QProgressBar{{"
                                    "border: 1px solid transparent;"
                                    "text-align: center;"
                                    "color: rgba({});"
                                    "border-radius: 8px;"
                                    "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, "
                                    "stop:0 rgba(207, 240, 158, 50), "
                                    "stop:1 rgba(209, 209, 209, 50));"
                                    "}}"
                                    "QProgressBar::chunk{{"
                                    "background-color: rgba(161,247,96,100);"
                                    "border-radius: 8px;"
                                    "border: 1px transparent;"
                                    "color: transparent;"
                                    "}}".format(self.colors['text']))
        self.progress.setAlignment(Qt.AlignCenter)
        self.progress.setFixedHeight(20)
        self.progress.setGeometry(
            12, self.height() - self.progress.height() - 24, self.width() - 40, 20
        )

    def mousePressEvent(self, _):
        pass


class MainUiSplash(BaseQWidget, WithSignal, ProgressInterface):

    def __init__(self, parent, main_ui_obj_name):
        BaseQWidget.__init__(self, _MainUiSplash(parent))
        WithSignal.__init__(self, sig_splash, main_ui_obj_name)

    @property
    def qobj(self) -> _MainUiSplash:
        return super(MainUiSplash, self).qobj

    def show(self, title: str = None, text: str = None, auto_close: bool = True):
        self.set_progress(0)
        self.qobj.show()

    def hide(self):
        self.qobj.finish(self.qobj)

    def set_progress(self, value: int):
        self.qobj.progress.setValue(value)

    def set_progress_text(self, value: str):
        self.qobj.progress.setFormat(value)

    def add_progress(self, value: int):
        self.set_progress(self.qobj.progress.value() + value)

    def set_current_text(self, value: str):
        pass

    def set_current_progress(self, value: int):
        pass

    def add_current_progress(self, value: int):
        pass

    def set_progress_title(self, value: str):
        pass

    def set_current_enabled(self, value: bool):
        pass
