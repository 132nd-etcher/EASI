# coding=utf-

from tests.init_ui import get_qt_app

if __name__ == '__main__':
    qt_app, main_ui = get_qt_app()
    main_ui.config_dialog.show()
    exit(qt_app.exec())
