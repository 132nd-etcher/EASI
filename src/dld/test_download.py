# coding=utf-8

from src.dld.download import downloader, DownloadFileList
from src.sig import sig_long_op_dialog, sig_long_op_dual_dialog
from tests.init_ui import get_qt_app

if __name__ == '__main__':

    def on_completion():
        print(dl.all_good())
        sig_long_op_dual_dialog.hide()

    qt_app, main_ui = get_qt_app()
    sig_long_op_dialog.show()
    sig_long_op_dialog.hide()
    sig_long_op_dual_dialog.show()
    dl = DownloadFileList()
    dl.add_file_from_github('132nd-etcher', 'kdiff3', 'Qt5Core.dll')
    dl.add_file_from_github('132nd-etcher', 'kdiff3', 'Qt5Gui.dll')
    dl.add_file_from_github('132nd-etcher', 'kdiff3', 'Qt5Widgets.dll')
    dl.add_file_from_github('132nd-etcher', 'kdiff3', 'kdiff3.exe')
    downloader.download_multiple_to_file(
        dl,
        progress=sig_long_op_dual_dialog,
        on_completion=on_completion
    )
    exit(qt_app.exec())
    # exit(qt_app.exec())
