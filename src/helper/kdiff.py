# coding=utf-8

import zipfile

from src.dld import downloader, FileDownload
from src.cfg import config
from src.low.custom_logging import make_logger
from src.low.custom_path import Path
from src.low.singleton import Singleton
from src.sig import sig_main_ui_states
from .abstract import AbstractHelper

logger = make_logger(__name__)


class KdiffHelper(AbstractHelper, metaclass=Singleton):

    @property
    def folder(self) -> Path:
        return self.path.dirname().abspath()

    @property
    def path(self) -> Path:
        return Path(config.kdiff_path)

    @path.setter
    def path(self, value: str or Path):
        if isinstance(value, Path):
            value = value.abspath()
        config.kdiff_path = value

    def install(self, wait=True):

        logger.info('installing KDiff3 in: {}'.format(self.path))

        def __install(_fdl: FileDownload):
            if _fdl.success:
                sig_main_ui_states.set_progress(0)
                sig_main_ui_states.set_progress_title('Unzipping KDiff3')
                with zipfile.ZipFile(_fdl.local_file) as _zip:
                    total = len(_zip.namelist())
                    count = 0
                    for name in _zip.namelist():
                        _zip.extract(name, '.')
                        count += 1
                        sig_main_ui_states.set_progress((count / total) * 100)
                p = Path('./kdiff3-master')
                p.rename('kdiff3')
                sig_main_ui_states.show_msg('Success', 'KDiff3 has been successfully installed !')
            else:
                raise RuntimeError('download failed')

        def __download():
            if self.folder.exists() and self.folder.isdir():
                logger.debug('removing old kdiff3 directory')
                self.folder.rmtree()
            sig_main_ui_states.set_progress_title('Installing KDIFF3')
            kwargs = dict(
                url=r'https://github.com/132nd-etcher/kdiff3/archive/master.zip',
                progress=sig_main_ui_states,
            )
            if not wait:
                kwargs['callback'] = __install
            _fdl = downloader.download(**kwargs)
            return _fdl

        fdl = __download()
        if wait:
            fdl.wait()
            __install(fdl)

    @property
    def is_installed(self) -> bool:
        if self.path.exists() and self.path.isfile():
            return True
        return False

    @property
    def name(self):
        return 'kdiff3'

    @property
    def download_link(self):
        return r'https://github.com/132nd-etcher/kdiff3/archive/master.zip'


kdiff = KdiffHelper()
