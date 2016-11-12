# coding=utf-8

import sys
import os

import src.__version__

FROZEN = hasattr(sys, 'frozen')
try:
    TESTING = os.environ['EASI_TESTING'] == '1'
except KeyError:
    TESTING = False
PATH_LOG_FILE = 'easi.debug'
PATH_CONFIG_FILE = 'easi.config'
PATH_KEYRING_FILE = 'easi.credentials'

APP_SHORT_NAME = 'EASI'
APP_FULL_NAME = 'Etcher\'s Automated Skin Installer'
APP_VERSION = src.__version__.__version__
APP_AUTHOR = 'etcher'
APP_STATUS = 'ALPHA'
APP_RELEASE_NAME = 'Another Fine Product From The Nonsense Factory'
APP_WEBSITE = r'https://github.com/132nd-etcher/EASI'

EASIMETA_REPO_URL = r'https://github.com/EASIMETA/EASIMETA.git'

GH_APP_USER = '132nd-etcher'
GH_APP_REPO = 'EASI'
GH_APP_REPO_TEST = 'EASI_tests'

DCS = {
    'reg_key': {
        'stable': 'DCS World',
        'beta': 'DCS World OpenBeta',
        'alpha': 'DCS World 2 OpenAlpha',
    },
}

QT_APP = None
MAIN_UI = None

try:
    # noinspection PyUnresolvedReferences
    from winreg import ConnectRegistry, HKEY_LOCAL_MACHINE, KEY_READ, KEY_WOW64_64KEY, OpenKey, QueryValueEx
    a_reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    try:
        with OpenKey(a_reg, r"SOFTWARE\Microsoft\Cryptography") as aKey:
            MACHINE_GUID = QueryValueEx(aKey, "MachineGuid")[0]
    except FileNotFoundError:
        try:
            with OpenKey(a_reg, r"SOFTWARE\Microsoft\Cryptography", access=KEY_READ | KEY_WOW64_64KEY) as aKey:
                MACHINE_GUID = QueryValueEx(aKey, "MachineGuid")[0]
        except FileNotFoundError:
            MACHINE_UID = False
except ImportError:
    MACHINE_UID = False
