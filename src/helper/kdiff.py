# coding=utf-8

import zipfile

from src.dld import downloader, FileDownload
from src.cfg.cfg import Config
from src.low.custom_logging import make_logger
from src.low.custom_path import Path
from src.low.singleton import Singleton
from src.sig import SigProgress, SigMsg
from src.helper.abstract import AbstractHelper, AbstractHelperRunProfile
from subprocess import Popen

logger = make_logger(__name__)


class KdiffHelper(AbstractHelper, metaclass=Singleton):

    def compare(self, base: Path, file2: Path, file3: Path = None,
                base_alias: str = None,
                file2_alias: str = None,
                file3_alias: str = None,
                output: Path = None):
        cmd = [self.path]
        cmd += ['-b', str(base.abspath())]
        cmd += [str(file2.abspath())]
        if file3:
            cmd += [str(file3.abspath())]
        if output:
            cmd += ['-o', str(output.abspath())]
        if base_alias:
            cmd += ['--L1', base_alias]
        if file2_alias:
            cmd += ['--L2', base_alias]
        if file3_alias:
            cmd += ['--L3', base_alias]
        cmd += ['--cs', 'Show Statusbar=0']
        cmd += ['--cs', 'TabSize=4']
        cmd += ['--cs', 'ShowInfoDialogs=0']
        cmd += ['--cs', 'CreateBakFiles=0']
        # if output:
        #     cmd.append('-o')
        #     cmd.append(str(output.abspath()))
        Popen(cmd)

    def run_profile(self, profile: AbstractHelperRunProfile):
        pass

    @property
    def folder(self) -> Path:
        return Path(self.path.dirname().abspath())

    @property
    def path(self) -> Path:
        return Path(Config().kdiff_path)

    @path.setter
    def path(self, value: str or Path):
        if isinstance(value, Path):
            value = value.abspath()
        Config().kdiff_path = value

    def download(self, wait=True):
        if self.folder.exists() and self.folder.isdir():
            logger.debug('removing old kdiff3 directory')
            self.folder.rmtree()
        SigProgress().show('Installing KDiff3...', 'Downloading...')
        kwargs = dict(
            url=self.download_link,
            progress=SigProgress(),
        )
        if not wait:
            kwargs['callback'] = self.install
        fdl = downloader.download(**kwargs)
        return fdl

    def install(self, fdl: FileDownload):
        if fdl.success:
            SigProgress().set_progress(0)
            SigProgress().set_progress_text('Unzipping KDiff3')
            with zipfile.ZipFile(fdl.local_file) as _zip:
                total = len(_zip.namelist())
                count = 0
                for name in _zip.namelist():
                    _zip.extract(name, '.')
                    count += 1
                    SigProgress().set_progress((count / total) * 100)
            p = Path('./kdiff3-master')
            p = p.rename(self.folder)
            Config().kdiff_path = Path(p.joinpath('kdiff3.exe')).abspath()
            SigMsg().show('Success', 'KDiff3 has been successfully installed !')
        else:
            raise RuntimeError('download failed')

    def download_and_install(self, wait=True):

        logger.info('installing KDiff3 in: {}'.format(self.path))
        fdl = self.download(wait)
        if wait:
            fdl.wait()
            self.install(fdl)

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
