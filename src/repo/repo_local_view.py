# coding=utf-8

import typing
import webbrowser

from blinker import Signal

from src.sig import SIG_LOCAL_REPO_CHANGED, SIG_INIT_VIEWS
from src.easi.ops import simple_input, confirm
from src.ui.base.table_view import BaseTableView, QModelIndex, QTableView
from src.repo.repo_local import LocalRepo
from src.repo.repo_view import RepoView
from src.repo.repo import Repo
from src.ui.dialog_repo.dialog import RepoDetailsDialog


class LocalRepoTableView(BaseTableView):

    def __init__(
            self,
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

        self.btns_add_button('Add', self.add_repository)
        self.btns_add_button('Remove', self.remove_repository, False)
        self.btns_insert_space()
        self.btns_add_button('Details', self.show_details_for_selected_repo, False)
        self.btns_add_button('Show on Github', self.show_on_github, False)
        self.btns_fill()

    @property
    def reset_model_signals(self) -> typing.List[Signal] or None:
        return [SIG_LOCAL_REPO_CHANGED, SIG_INIT_VIEWS]

    def on_double_click(self, index: QModelIndex):
        self.show_details_for_selected_repo()

    def on_click(self, index: QModelIndex):
        self.btns_set_enabled(True)
        if any({
            self.selected_row.name == 'EASIMETA',
            self.selected_row == LocalRepo().own_meta_repo
        }):
            self.btns_get('Remove').setEnabled(False)

    def on_show(self, *args, **kwargs):
        print('on show')
        self.btns_set_enabled(False)
        self.set_updates_enabled(True)

    def on_hide(self, *args, **kwargs):
        print('on hide')
        self.set_updates_enabled(False)

    def show_details_for_selected_repo(self):
        RepoDetailsDialog(self.selected_row, self.table).qobj.exec()
        self.resize_columns()

    def show_on_github(self):
        webbrowser.open_new_tab(self.selected_row.github_url)

    @property
    def selected_row(self) -> Repo:
        return BaseTableView.selected_row.fget(self)

    def build_model(self):
        self.reset_table_data()
        for repo in LocalRepo().repos:
            repo_view = RepoView(repo)
            self.add_row(repo_view)

    @property
    def table_headers(self) -> list:
        return ['Github username', 'Push permission']

    def row_changed(self, row: int):
        pass

    def add_repository(self):
        self.table.setUpdatesEnabled(False)
        repo_owner = simple_input(
            title='Adding repository',
            parent=self.table
        )
        if repo_owner:
            LocalRepo().add_repo(repo_owner)
        self.table.setUpdatesEnabled(True)

    def remove_repository(self):
        self.table.setUpdatesEnabled(False)
        if confirm(
                'Are you sure you want to remove this repository ?\n\n'
                '(the repository will be deleted the next time EASI starts)',
                'Removing: {}'.format(self.selected_row.name)
        ):
            LocalRepo().remove_repo(self.selected_row.name)
        self.table.setUpdatesEnabled(True)
