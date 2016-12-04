# coding=utf-8

import typing
import os
import webbrowser
from collections import OrderedDict

from src.sig import SigProgress

from blinker import Signal
from blinker_herald import signals

from src.sig import SIG_LOCAL_REPO_CHANGED, SIG_INIT_VIEWS
from src.easi.ops import simple_input, confirm
from src.ui.base.table_view import BaseTableView, QModelIndex, QTableView
from src.mod.mod import Mod
from src.mod.mod_file_view import ModFileView, DeletedModFileView
from src.repo.repo import Repo
from src.cache.cache_event import CacheEvent
from src.qt import pyqtSignal, QTimer, QMenu, QCursor
from src.threadpool.threadpool import ThreadPool
from src.mod.mod_file import ModFile


class ModFilesView(BaseTableView):
    sig_refresh = pyqtSignal(name='ModFilesView_refresh')

    def __init__(
            self,
            mod: Mod,
            qt_table_view: QTableView,
            sorting_enabled: bool = True,
            parent=None,
            btns_layout=None):
        BaseTableView.__init__(
            self,
            qt_table_view=qt_table_view,
            sorting_enabled=sorting_enabled,
            parent=parent,
            btns_layout=btns_layout)

        self.__mod = mod

        self.pool = ThreadPool(1, 'mod_files', True)

        self.refresh_scheduler = QTimer(self)
        # noinspection PyUnresolvedReferences
        self.refresh_scheduler.timeout.connect(self.reset_model)
        self.sig_refresh.connect(self.start_timer)

        # noinspection PyUnusedLocal
        def cache_signal_handler(sender, signal_emitter, event: CacheEvent):
            if event.filter(self.__mod.local_folder.abspath()):
                self.sig_refresh.emit()

        self.cache_signal_handler = cache_signal_handler
        menu = QMenu()
        self.__menu = {
            'menu': menu,
            'open': menu.addAction('Open'),
            'delete': menu.addAction('Delete')
        }

        self.btns_add_button('Open mod folder', self.open_mod_folder_in_explorer)
        self.btns_insert_space()
        self.btns_add_button('Show file', self.show_file_in_explorer, False)
        self.btns_add_button('Open file', self.open_file_in_explorer, False)
        self.btns_insert_space()
        self.btns_add_button('Save', self.save)
        self.btns_add_button('Reset', self.reset)
        self.btns_fill()

    def context_menu(self, event):
        if self.selected_row:
            action = self.__menu['menu'].exec(QCursor.pos())
            if action == self.__menu['open']:
                self.open_file_in_explorer()
            else:
                raise NotImplementedError

    def start_timer(self):
        self.refresh_scheduler.start(500)

    @property
    def reset_model_signals(self) -> typing.List[Signal] or None:
        return [SIG_INIT_VIEWS]

    def on_double_click(self, index: QModelIndex):
        self.open_file_in_explorer()

    def on_click(self, index: QModelIndex):
        self.btns_set_enabled(True)

    def on_show(self, *args, **kwargs):
        signals.post_cache_changed_event.connect(self.cache_signal_handler, weak=False)
        self.reset_model()
        self.set_updates_enabled(True)

    def on_hide(self, *args, **kwargs):
        self.set_updates_enabled(False)
        signals.post_cache_changed_event.disconnect(self.cache_signal_handler)

    @property
    def selected_row(self) -> ModFile:
        return BaseTableView.selected_row.fget(self)

    def build_model(self):
        self.refresh_scheduler.stop()
        self.reset_table_data()
        total = len(self.__mod.local_files) + len(self.__mod.deleted_local_files)
        count = 0
        SigProgress().show('Updating local files...', '')
        for mod_file in self.__mod.local_files:
            self.add_row(ModFileView(mod_file))
            count += 1
            SigProgress().set_progress((count / total) * 100)
        for deleted_mod_file in self.__mod.deleted_local_files:
            self.add_row(DeletedModFileView(deleted_mod_file))
            count += 1
            SigProgress().set_progress((count / total) * 100)

    @property
    def table_headers(self) -> list:
        return ['File', 'Size', 'Last changed', 'Status', 'Action']

    def row_changed(self, row: int):
        pass

    def open_file_in_explorer(self):
        os.startfile(str(self.selected_row.abspath))

    def show_file_in_explorer(self):
        os.startfile(str(self.selected_row.abspath.dirname()))

    def open_mod_folder_in_explorer(self):
        os.startfile(str(self.__mod.local_folder.abspath()))

    def __save(self):
        self.qt_table.setUpdatesEnabled(False)
        SigProgress().show('Saving metadata...', '')
        files = list(self.__mod.local_files)
        current = 0
        d = OrderedDict()
        for mod_file in files:
            SigProgress().set_progress_text(mod_file.rel_path)
            d[str(mod_file.rel_path)] = mod_file.meta
            current += 1
            SigProgress().set_progress((current / len(files)) * 100)
        self.__mod.meta.files = d
        self.__mod.meta.write()
        self.qt_table.setUpdatesEnabled(True)
        self.reset_model()

    def save(self):
        self.pool.queue_task(self.__save)

    def reset(self):
        raise NotImplementedError
