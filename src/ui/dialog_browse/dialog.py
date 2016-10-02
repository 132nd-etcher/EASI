# coding=utf-8

import typing

from src.low.custom_path import Path
from src.qt import *


class BrowseDialog(QFileDialog):
    def __init__(self, parent, title: str):
        QFileDialog.__init__(self, parent)
        self.setWindowIcon(QIcon(qt_resources.app_ico))
        self.setViewMode(QFileDialog.Detail)
        self.setWindowTitle(title)

    def parse_single_result(self) -> Path or None:
        if self.exec():
            result = self.selectedFiles()[0]
            return Path(result)
        else:
            return None

    def parse_multiple_results(self) -> typing.List[Path] or None:
        if self.exec():
            results = [Path(x) for x in self.selectedFiles()[0]]
            return results
        else:
            return None

    @staticmethod
    def make(parent, title: str, filter: typing.List[str] = None, init_dir: str = '.'):
        if filter is None:
            filter = ['*.*']
        dialog = BrowseDialog(parent, title)
        dialog.setOption(QFileDialog.DontResolveSymlinks)
        dialog.setOption(QFileDialog.DontUseCustomDirectoryIcons)
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setNameFilters(filter)
        dialog.setDirectory(init_dir)
        dialog.setAcceptMode(QFileDialog.AcceptOpen)
        dialog.setOption(QFileDialog.ReadOnly)
        return dialog

    @staticmethod
    def get_file(parent, title: str, _filter: typing.List[str] = None, init_dir: str = '.') -> Path or None:
        dialog = BrowseDialog.make(parent, title, _filter, init_dir)
        dialog.setFileMode(QFileDialog.AnyFile)
        return dialog.parse_single_result()

    @staticmethod
    def get_existing_file(parent, title: str, _filter: typing.List[str] = None, init_dir: str = '.') -> Path or None:
        dialog = BrowseDialog.make(parent, title, _filter, init_dir)
        dialog.setFileMode(QFileDialog.ExistingFile)
        return dialog.parse_single_result()

    @staticmethod
    def get_existing_files(parent, title: str, _filter: typing.List[str] = None,
                           init_dir: str = '.') -> typing.List[Path] or None:
        dialog = BrowseDialog.make(parent, title, _filter, init_dir)
        dialog.setFileMode(QFileDialog.ExistingFiles)
        return dialog.parse_multiple_results()

    @staticmethod
    def save_file(parent, title: str, _filter: typing.List[str] = None, init_dir: str = '.') -> Path or None:
        dialog = BrowseDialog.make(parent, title, _filter, init_dir)
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        return dialog.parse_single_result()

    @staticmethod
    def get_directory(parent, title: str, init_dir: str = '.') -> Path or None:
        dialog = BrowseDialog.make(parent, title, init_dir=init_dir)
        dialog.setFileMode(QFileDialog.Directory)
        dialog.setOption(QFileDialog.ShowDirsOnly)
        return dialog.parse_single_result()
