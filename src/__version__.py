# coding=utf-8

import sys
import subprocess
from json import loads
from src.low.custom_path import Path

if hasattr(sys, 'frozen'):
    __version__ = Path(sys.executable).get_win32_file_info().file_version
else:
    __version__ = loads(subprocess.check_output(['gitversion']).decode().rstrip()).get('FullSemVer')


__guid__ = '4ae6dbb7-5b26-43c6-b797-2272f5a074f3'
