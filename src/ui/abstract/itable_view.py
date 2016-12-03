# coding=utf-8

import abc
import typing
from abc import abstractmethod, abstractproperty

from blinker import Signal

from src.qt import QAbstractTableModel, QModelIndex, QVariant, QTableView
from src.ui.abstract.itable_view_row import ITableViewRow
from src.ui.abstract.iview import IView


class ITableView(QAbstractTableModel, IView):

    @property
    @abc.abstractproperty
    def reset_model_signals(self) -> typing.List[Signal] or None:
        """Optional signal to trigger a model reset"""

    @abc.abstractmethod
    def add_row(self, row: ITableViewRow):
        pass

    @abc.abstractmethod
    def remove_row(self, row: int):
        pass

    @abc.abstractmethod
    def row_changed(self, row: int):
        pass

    @property
    @abc.abstractproperty
    def table_headers(self) -> list:
        pass

    @abc.abstractmethod
    def data(self, index: QModelIndex, role=None) -> QVariant:
        pass

    @abc.abstractmethod
    def headerData(self, column: int, orientation: int, role=None) -> QVariant:
        pass

    @abc.abstractmethod
    def flags(self, index: QModelIndex):
        pass

    @abc.abstractmethod
    def rowCount(self, parent=None, *args, **kwargs):
        pass

    @abc.abstractmethod
    def columnCount(self, parent=None, *args, **kwargs):
        pass

    @abc.abstractmethod
    def on_click(self, index: QModelIndex):
        pass

    @abc.abstractmethod
    def on_double_click(self, index: QModelIndex):
        pass

    @abstractmethod
    def reset_table_data(self):
        pass

    @property
    @abstractproperty
    def table_data(self) -> list:
        pass

    @property
    @abstractproperty
    def qt_table(self) -> QTableView:
        pass

    @abstractmethod
    def set_updates_enabled(self, value: bool):
        pass
