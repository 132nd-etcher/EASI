# coding=utf-8

import blinker

from src.qt import *

sig_main_ui_style = blinker.signal('sig_main_ui_style')


@sig_main_ui_style.connect
def change_style(_, style):
    print(style)
    f_style = QStyleFactory()
    print(f_style.keys())
    style = f_style.create(style)
    print(style)
    QApplication.setStyle(style)
