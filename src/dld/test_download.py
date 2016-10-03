# coding=utf-8

# from src.dld.download import downloader, DownloadFileList
from src.dld.download import downloader, FileDownload, BulkFileDownload
from src.sig import sig_long_op_dialog
from tests.init_ui import get_qt_app

if __name__ == '__main__':

    def on_completion(_fdl):
        print(_fdl.success)

    qt_app, main_ui = get_qt_app()
    sig_long_op_dialog.show()
    # fdl = downloader.download(
    #     r'https://raw.githubusercontent.com/132nd-etcher/kdiff3/master/Qt5Core.dll',
    #     progress=sig_long_op_dialog,
    #     callback=on_completion
    # )
    # fdl2 = downloader.download(
    #     r'https://raw.githubusercontent.com/132nd-etcher/kdiff3/master/Qt5Gui.dll',
    #     progress=sig_long_op_dialog,
    #     callback=on_completion
    # )

    file_list = [
        r'http://www.textfiles.com/100/914bbs.txt',
        r'http://www.textfiles.com/100/ad.txt',
        r'http://www.textfiles.com/100/adventur.txt',
        r'http://www.textfiles.com/100/arttext.fun',
        r'http://www.textfiles.com/100/bc760mod.ham',
        r'http://www.textfiles.com/100/black.box',
        r'http://www.textfiles.com/100/cDc-0200.txt',
        r'http://www.textfiles.com/100/crossbow',
        r'http://www.textfiles.com/100/gems.txt',
        r'http://www.textfiles.com/100/krckwczt.app',
    ]
    fdl_list = []
    for x in file_list:
        fdl_list.append(FileDownload(x))

    fdl1 = FileDownload(r'https://raw.githubusercontent.com/132nd-etcher/kdiff3/master/Qt5Core.dll')
    fdl2 = FileDownload(r'https://raw.githubusercontent.com/132nd-etcher/kdiff3/master/Qt5Gui.dll')
    downloader.bulk_download(fdl_list, progress=sig_long_op_dialog)
    # fdl = downloader.download_in_background(
    #     r'https://raw.githubusercontent.com/132nd-etcher/kdiff3/master/Qt5Core.dlll',
    #     progress=sig_long_op_dialog,
    #     callback=on_completion
    # )
    # print('success', fdl.success)
    # sig_long_op_dialog.show()
    # sig_long_op_dialog.hide()
    # sig_long_op_dialog.show()
    # dl = DownloadFileList()
    # dl.add_file_from_github('132nd-etcher', 'kdiff3', 'Qt5Core.dll')
    # dl.add_file_from_github('132nd-etcher', 'kdiff3', 'Qt5Gui.dll')
    # dl.add_file_from_github('132nd-etcher', 'kdiff3', 'Qt5Widgets.dll')
    # dl.add_file_from_github('132nd-etcher', 'kdiff3', 'kdiff3.exe')
    # downloader.download_multiple_to_file(
    #     dl,
    #     progress=sig_long_op_dialog,
    #     on_completion=on_completion
    # )
    exit(qt_app.exec())
    # exit(qt_app.exec())
