# coding=utf-8
from tests.init_ui import get_qt_app

if __name__ == '__main__':
    get_qt_app()

    from src.ui.dialog_msg.dialog import MsgDialog

    print(MsgDialog.make('some text'))
