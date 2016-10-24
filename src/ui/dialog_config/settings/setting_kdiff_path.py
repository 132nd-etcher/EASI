# coding=utf-8

from src.helper.kdiff import kdiff
from blinker import signal
from src.low.custom_logging import make_logger
from src.low.custom_path import Path
from src.qt import QToolButton, QAction, QLineEdit, QIcon
from src.ui.dialog_config.settings.abstract_path_setting import AbstractPathSetting
from src.ui.dialog_browse.dialog import BrowseDialog

logger = make_logger(__name__)


class KDiffPathSetting(AbstractPathSetting):

    def __init__(self, dialog):
        AbstractPathSetting.__init__(self, dialog)
        self.q_action_install_kdiff = QAction(QIcon(':/pic/download.png'), 'Install now', self.dialog)
        self.dialog.kdiff_line_edit.addAction(self.q_action_install_kdiff, QLineEdit.TrailingPosition)

        def on_path_changed(_, value):
            self.set_dialog_value(value)

        signal('Config_kdiff_path_value_changed').connect(on_path_changed, weak=False)

    @property
    def value_name(self) -> str:
        return 'kdiff_path'

    @property
    def qt_menu_btn(self) -> QToolButton:
        return self.dialog.btn_kdiff

    @property
    def value_display_name(self) -> str:
        return 'kdiff3.exe'

    @staticmethod
    def download_kdiff():
        kdiff.download_and_install(wait=False)

    def save_to_meta(self):
        if self.get_value_from_dialog() is None:
            return True
        else:
            return super(KDiffPathSetting, self).save_to_meta()

    def validate_dialog_value(self) -> bool:
        if self.get_value_from_dialog():
            p = Path(self.get_value_from_dialog())
            if not p.exists():
                self.show_error_balloon('File does not exist')
            elif not p.isfile():
                self.show_error_balloon('Not a file')
            elif not p.basename() == 'kdiff3.exe':
                self.show_error_balloon('Expected a file named "kdiff3.exe"')
            else:
                return True
        else:
            return True

    def setup(self):
        self.menu.addAction(self.q_action_install_kdiff)
        super(KDiffPathSetting, self).setup()
        # noinspection PyUnresolvedReferences
        self.q_action_install_kdiff.triggered.connect(self.download_kdiff)

    def browse_for_value(self):
        init_dir = Path(self.get_value_from_dialog()).abspath().dirname()
        if init_dir is None:
            init_dir = 'c:/users'
        path = BrowseDialog.get_existing_file(
            parent=self.dialog,
            title='Select the kdiff3.exe file',
            init_dir=init_dir,
            _filter=['kdiff3.exe']
        )
        if path:
            self.qt_object.setText(str(path.abspath()))

    def get_value_from_dialog(self):
        if self.qt_object.text():
            return self.qt_object.text()
        else:
            return None

    @property
    def qt_object(self):
        return self.dialog.kdiff_line_edit
