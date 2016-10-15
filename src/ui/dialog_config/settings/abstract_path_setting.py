import abc
import os

from src.low.custom_path import Path
from src.qt import QMenu, QAction, QToolButton, QIcon, QLineEdit
from src.ui.dialog_browse.dialog import BrowseDialog
from src.ui.dialog_config.settings.abstract_config import AbstractConfigSetting
from src.sig import SignalReceiver


class AbstractPathSetting(AbstractConfigSetting):
    def __init__(self, dialog, path_changed_sig):
        AbstractConfigSetting.__init__(self, dialog)
        self.menu = QMenu(self.dialog)
        self.q_action_browse = QAction(QIcon(':/pic/fs_browse.png'), 'Change location', self.dialog)
        self.q_action_show = QAction(QIcon(':/pic/fs_open.png'), 'Show in explorer', self.dialog)
        self.receiver = SignalReceiver(self)
        self.receiver[path_changed_sig] = self.on_path_changed

    @property
    def qt_object(self) -> QLineEdit:
        return super(AbstractPathSetting, self).qt_object()

    def on_path_changed(self, value):
        self.set_dialog_value(value)

    def dialog_has_changed_methods(self) -> list:
        return [self.qt_object.textChanged]

    def browse_for_value(self):
        init_dir = self.value
        if init_dir is None:
            init_dir = 'c:/users'
        path = BrowseDialog.get_directory(
            parent=self.dialog,
            title='Select your {} directory'.format(self.dir_name()),
            init_dir=init_dir
        )
        if isinstance(path, Path) and path.exists():
            self.qt_object.setText(str(path.abspath()))

    def show_in_explorer(self):
        os.startfile(self.value)

    # noinspection PyUnresolvedReferences
    def setup(self):
        self.menu.addAction(self.q_action_browse)
        self.menu.addAction(self.q_action_show)
        self.qt_menu_btn.setMenu(self.menu)
        self.q_action_browse.triggered.connect(self.browse_for_value)
        self.q_action_show.triggered.connect(self.show_in_explorer)
        self.qt_object.textChanged.connect(self.remove_balloons)

    def get_value_from_dialog(self):
        return self.qt_object.text()

    def set_dialog_value(self, value: str):
        self.qt_object.setText(str(value))

    @abc.abstractmethod
    def dir_name(self) -> str:
        """"""

    @property
    @abc.abstractproperty
    def qt_menu_btn(self) -> QToolButton:
        """"""

    def validate_dialog_value(self) -> bool:
        p = Path(self.get_value_from_dialog())
        if not p.exists():
            self.show_error_balloon('Directory does not exist')
        elif not p.isdir():
            self.show_error_balloon('Not a directory')
        else:
            return True
