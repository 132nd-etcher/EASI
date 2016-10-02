# coding=utf-

from tests.init_ui import get_qt_app

if __name__ == '__main__':
    qt_app = get_qt_app()
    from src.ui.dialog_browse.dialog import BrowseDialog
    print(BrowseDialog.get_directory(None, 'title', init_dir='.'))
    exit(0)
