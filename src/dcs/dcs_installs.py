# coding=utf-8

try:
    import winreg
except ImportError:
    from unittest.mock import MagicMock

    winreg = MagicMock()
from typing import Tuple

from blinker_herald import emit
from src.cfg import Config
from src.low.custom_logging import make_logger
from src.low.custom_path import Path
from src.low.singleton import Singleton
from src.newsig.sigprogress import SigProgress

logger = make_logger(__name__)

A_REG = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)


def look_for_saved_games_path():
    if Config().saved_games_path is None:
        logger.debug('searching for base "Saved Games" folder')
        try:
            logger.debug('trying "User Shell Folders"')
            with winreg.OpenKey(A_REG,
                                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders") as aKey:
                # noinspection SpellCheckingInspection
                base_sg = Path(winreg.QueryValueEx(aKey, "{4C5C32FF-BB9D-43B0-B5B4-2D72E54EAAA4}")[0])
        except FileNotFoundError:
            logger.debug('failed, trying "Shell Folders"')
            try:
                with winreg.OpenKey(A_REG,
                                    r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders") as aKey:
                    # noinspection SpellCheckingInspection
                    base_sg = Path(winreg.QueryValueEx(aKey, "{4C5C32FF-BB9D-43B0-B5B4-2D72E54EAAA4}")[0])
            except FileNotFoundError:
                logger.debug('darn it, another fail, falling back to "~"')
                base_sg = Path('~').expanduser().abspath()
        Config().saved_games_path = str(base_sg.abspath())
        return base_sg
    else:
        return Path(Config().saved_games_path)


class DCSInstalls(metaclass=Singleton):
    def __init__(self):
        self.base_sg = None
        self.installs = {
            'stable': {
                'reg_key': 'DCS World',
                'sg_default': 'DCS',
                'install': None,
                'sg': None,
                'version': None,
            },
            'beta': {
                'reg_key': 'DCS World OpenBeta',
                'sg_default': 'DCS.openbeta',
                'install': None,
                'sg': None,
                'version': None,
            },
            'alpha': {
                'reg_key': 'DCS World 2 OpenAlpha',
                'sg_default': 'DCS.openalpha',
                'install': None,
                'sg': None,
                'version': None,
            },
        }

    # noinspection PyBroadException
    @emit()
    def discover_dcs_installation(self):
        logger.debug('looking for DCS installations paths')
        progress = SigProgress()
        progress.set_progress_title('Looking for DCS installations')

        self.base_sg = look_for_saved_games_path()
        logger.debug('using "Saved Games" folder: {}'.format(Config().saved_games_path))

        logger.debug('found base "Saved Games" path: {}'.format(self.base_sg.abspath()))
        progress.set_progress(20)
        partial_progress = 80 / len(self.installs)
        for k in self.installs:
            logger.debug('{}: searching for paths'.format(k))
            try:
                with winreg.OpenKey(A_REG, r'Software\Eagle Dynamics\{}'.format(self.installs[k]['reg_key'])) as aKey:
                    install_path = Path(winreg.QueryValueEx(aKey, "Path")[0])
                    self.installs[k]['install'] = install_path.abspath()
                    exe = Path(install_path.joinpath('run.exe'))
                    if exe.exists():
                        self.installs[k]['version'] = exe.get_win32_file_info().file_version
                    logger.debug('{}: install found: {}'.format(k, install_path.abspath()))
                logger.debug('{}: looking for "Saved Games" path'.format(k))
                variant_path = Path(install_path.joinpath('dcs_variant.txt'))
                logger.debug('{}: looking for variant: {}'.format(k, variant_path.abspath()))
                if variant_path.exists():
                    logger.debug('{}: found variant: "{}"; reading'.format(k, variant_path.abspath()))
                    self.installs[k]['sg'] = self.base_sg.abspath().joinpath('DCS.{}'.format(variant_path.text()))
                    logger.debug('{}: set "Saved Games" path to: {}'.format(k, self.installs[k]['sg']))
                else:
                    self.installs[k]['sg'] = self.base_sg.abspath().joinpath(self.installs[k]['sg_default'])
                    logger.debug('{}: no variant, falling back to default: {}'.format(k, self.installs[k]['sg']))
            except FileNotFoundError:
                logger.debug('no install path found for {}'.format(k))
                progress.add_progress(partial_progress)
        progress.set_progress(100)

    def __get_props(self, channel):
        return self.installs[channel]['install'], self.installs[channel]['sg'], self.installs[channel]['version']

    @property
    def stable(self) -> Tuple[Path, Path, str]:
        return self.__get_props('stable')

    @property
    def beta(self) -> Tuple[Path, Path, str]:
        return self.__get_props('beta')

    @property
    def alpha(self) -> Tuple[Path, Path, str]:
        return self.__get_props('alpha')


def init_dcs_installs():
    logger.info('dcs_installs: looking for DCS installation in Windows registry')
    DCSInstalls().discover_dcs_installation()
    logger.info('dcs_installs: lookup done')
