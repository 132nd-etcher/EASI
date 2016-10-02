# coding=utf-8

from tests.init_ui import get_qt_app


if __name__ == '__main__':
    qt_app, main_ui = get_qt_app()
    from src.ui.dialog_disclaimer.dialog import DisclaimerDialog
    print(DisclaimerDialog.make())
    qt_app.exit()
    exit(0)
