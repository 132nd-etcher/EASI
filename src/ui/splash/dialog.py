# coding=utf-8


from src.abstract import AbstractConnectedQObject, AbstractSplash
from src.low import constants
from src.qt import QSplashScreen, QPixmap, qt_resources, Qt, QLabel, QFont, QProgressBar
from src.sig import sig_splash


class CustomSplash(QSplashScreen):
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


# class MainUiSplash(AbstractConnectedQObject, SplashInterface):
class MainUiSplash(AbstractConnectedQObject, AbstractSplash):
    def __init__(self, parent, main_ui_obj_name):
        AbstractConnectedQObject.__init__(self, sig_splash, main_ui_obj_name, CustomSplash(parent))

    def get(self) -> QSplashScreen:
        s = self.qobj
        assert isinstance(s, QSplashScreen)
        return s

    def get_progress(self) -> QProgressBar:
        p = self.qobj.progress
        assert isinstance(p, QProgressBar)
        return p

    def current_progress(self):
        return self.get_progress().value()

    def add_to_progress(self, value: int):
        self.set_progress(self.current_progress() + value)

    def show(self):
        self.set_progress(0)
        self.qobj.show()

    def kill(self):
        self.qobj.finish(self.qobj)

    def set_progress(self, value: int):
        self.get_progress().setValue(value)

    def set_text(self, value: str):
        self.get_progress().setFormat(value)
