# coding=utf-8

from src.keyring import keyring
from src.mod.factory import ModFactory
from tests.init_ui import get_qt_app

if __name__ == '__main__':
    qt_app = get_qt_app()
    keyring.init_keyring()
    t = ModFactory.make_draft()
    if t:
        t.meta.path = './test'
        t.meta.write()
