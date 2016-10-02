# coding=utf-

from tests.init_ui import get_qt_app

if __name__ == '__main__':
    qt_app = get_qt_app()
    from src.ui.dialog_feedback.dialog import FeedbackDialog
    FeedbackDialog.make()
    exit(qt_app.exec())
