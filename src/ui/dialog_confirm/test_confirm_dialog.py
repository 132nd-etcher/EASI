# coding=utf-8

from tests.init_ui import get_qt_app

if __name__ == '__main__':
    qt_app, main_ui = get_qt_app()
    from src.ui.dialog_confirm.dialog import ConfirmDialog
    print(ConfirmDialog.make('are you sure?'))
    qt_app.exit()
    exit(0)
