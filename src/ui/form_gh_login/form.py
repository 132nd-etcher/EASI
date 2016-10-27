# coding=utf-8

from src.qt import QWidget, Qt
from src.ui.form_gh_login.setting import GithubSetting
from src.ui.skeletons.form_gh_login import Ui_Form


class GHLoginForm(Ui_Form, QWidget):
    def __init__(self, parent, default_btn):
        QWidget.__init__(self, parent, flags=Qt.Widget)
        self.setupUi(self)
        self.setting = GithubSetting(self, default_btn)

    def setup(self):
        self.setting.setup()

    def on_show(self):
        self.setting.show()
