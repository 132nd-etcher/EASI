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
PATH_DCS_KNOWN_INSTALL = 'easi.dcs_installs'

APP_SHORT_NAME = 'EASI'
APP_FULL_NAME = 'Etcher\'s Automated Skin Installer'
APP_VERSION = src.__version__.__version__
APP_AUTHOR = 'etcher'
APP_STATUS = 'alpha'
APP_RELEASE_NAME = 'Another Fine Product From The Nonsense Factory'
APP_WEBSITE = r'https://github.com/132nd-etcher/EASI'

GH_APP_USER = '132nd-etcher'
GH_APP_REPO = 'EASI'
GH_APP_REPO_TEST = 'EASI_tests'

QT_APP = None
MAIN_UI = None

MACHINE_GUID = None
