# coding=utf-8

import os

from src.cfg import config
from src.qt import *
from src.ui.dialog_browse.dialog import BrowseDialog
from src.ui.dialog_msg.dialog import MsgDialog
from src.ui.skeletons.config_dialog import Ui_Settings
from .abstract_config_dialog_child import AbstractConfigDialogChild


class PathsSettings(AbstractConfigDialogChild):
    def setup(self):
        pass

    def __init__(self, dialog: Ui_Settings):
        self.dialog = dialog

        self.sg_menu = QMenu(self.dialog)
        self.qact_sg_browse = QAction('Change location', self.dialog)
        self.qact_sg_show = QAction('Show in explorer', self.dialog)
        self.sg_menu.addAction(self.qact_sg_browse)
        self.sg_menu.addAction(self.qact_sg_show)
        self.dialog.btn_sg.setMenu(self.sg_menu)

        self.cache_menu = QMenu(self.dialog)
        self.qact_cache_browse = QAction('Change location', self.dialog)
        self.qact_cache_show = QAction('Show in explorer', self.dialog)
        self.cache_menu.addAction(self.qact_cache_browse)
        self.cache_menu.addAction(self.qact_cache_show)
        self.dialog.btn_cache.setMenu(self.cache_menu)

        self.connect_qactions()

    # noinspection PyUnresolvedReferences
    def connect_qactions(self):
        self.qact_sg_browse.triggered.connect(self.browse_for_sg)
        self.qact_sg_show.triggered.connect(self.show_sg)
        self.qact_cache_browse.triggered.connect(self.browse_for_cache)
        self.qact_cache_show.triggered.connect(self.show_cache)

    def show_sg(self):
        os.startfile(config.saved_games_path)

    def show_cache(self):
        try:
            os.startfile(config.cache)
        except FileNotFoundError:
            pass

    def browse_for_cache(self):
        cache_path = BrowseDialog.get_directory(
            parent=self.dialog,
            title='Select your Saved Games directory',
            init_dir=config.cache
        )
        if cache_path:
            self.dialog.cache_line_edit.setText(str(cache_path.abspath()))

    def browse_for_sg(self):
        init_dir = config.saved_games_path
        if init_dir is None:
            init_dir = 'c:/users'
        sg_path = BrowseDialog.get_directory(
            parent=self.dialog,
            title='Select your Saved Games directory',
            init_dir=init_dir
        )
        if sg_path:
            self.dialog.sg_line_edit.setText(str(sg_path.abspath()))

    def load_settings(self):
        self.dialog.sg_line_edit.setText(config.saved_games_path)
        self.dialog.cache_line_edit.setText(config.cache)

    def save_settings(self):
        success = True
        path = self.dialog.sg_line_edit.text()
        try:
            config.saved_games_path = path
        except FileNotFoundError:
            MsgDialog.make(
                text='Path not found:\n\n{}'.format(path),
                title='Cannot save Saved Games path',
                parent=self.dialog
            )
            success = False
        except TypeError:
            MsgDialog.make(
                text='Not a directory:\n\n{}'.format(path),
                title='Cannot save Saved Games path',
                parent=self.dialog
            )
            success = False
        path = self.dialog.cache_line_edit.text()
        try:
            config.cache = path
        except TypeError:
            MsgDialog.make(
                text='Not a directory:\n\n{}'.format(path),
                title='Cannot save cache path',
                parent=self.dialog
            )
            success = False
        except ValueError:
            MsgDialog.make(
                text='Directory is not empty:\n\n{}'.format(path),
                title='Cannot save cache path',
                parent=self.dialog
            )
            success = False
        return success
