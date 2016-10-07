# coding=utf-8
import shutil
import zipfile

from src.dld import downloader, FileDownload
from src.low.custom_path import Path
from src.low.custom_logging import make_logger
from src.qt import QToolButton, QAction, QLineEdit, QIcon
from src.sig import sig_long_op_dialog, sig_msgbox
from src.ui.dialog_config.settings.abstract_path_setting import AbstractPathSetting
from ...dialog_browse.dialog import BrowseDialog

logger = make_logger(__name__)


class KDiffPathSetting(AbstractPathSetting):
    def __init__(self, dialog, value_name):
        AbstractPathSetting.__init__(self, dialog, value_name)
        self.q_action_install_kdiff = QAction(QIcon(':/pic/download.png'), 'Install now', self.dialog)
        self.dialog.kdiff_line_edit.addAction(self.q_action_install_kdiff, QLineEdit.TrailingPosition)

    @property
    def qt_menu_btn(self) -> QToolButton:
        return self.dialog.btn_kdiff

    def dir_name(self) -> str:
        return 'kdiff3.exe'

    def download_kdiff(self):
        p = Path('./kdiff3')
        if p.exists() and p.isdir():
            logger.debug('removing old kdiff3 directory')
            p.removedirs_p()
        sig_long_op_dialog.show('Installing KDiff3...', '')
        downloader.download(
            url=r'https://github.com/132nd-etcher/kdiff3/archive/master.zip',
            progress=sig_long_op_dialog,
            callback=self.install_kdiff
        )

    def install_kdiff(self, fdl: FileDownload):
        if fdl.success:
            sig_long_op_dialog.set_progress(0)
            sig_long_op_dialog.set_current_text('Unzipping...')
            with zipfile.ZipFile(fdl.local_file) as _zip:
                total = len(_zip.namelist())
                count = 0
                for name in _zip.namelist():
                    _zip.extract(name, '.')
                    count += 1
                    sig_long_op_dialog.set_progress((count / total) * 100)
            shutil.move('kdiff3-master', 'kdiff3')
            sig_long_op_dialog.hide()
            sig_msgbox.show('Success', 'KDiff3 has been successfully installed !')
            self.dialog.kdiff_line_edit.setText(Path('./kdiff3/kdiff3.exe').abspath())
        else:
            raise RuntimeError('download failed')

    def show(self):
        pass

    def save_to_meta(self):
        if self.get_value_from_dialog() is None:
            return True
        else:
            return super(KDiffPathSetting, self).save_to_meta()

    def validate_dialog_value(self) -> bool:
        if self.get_value_from_dialog():
            p = Path(self.get_value_from_dialog())
            if not p.exists():
                self.show_tooltip('File does not exist')
            elif not p.isfile():
                self.show_tooltip('Not a file')
            else:
                return True
        else:
            return True

    def set_dialog_value(self, value):
        self.dialog.kdiff_line_edit.setText(value)

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
            title='Select the kdiff3.exe file'.format(self.dir_name()),
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
