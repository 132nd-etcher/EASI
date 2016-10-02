# coding=utf-8

main_ui = None


def get_qt_app():
    try:
        from src.main import main
        return main(init_only=True, test_run=True)
    except SystemExit:
        pass
