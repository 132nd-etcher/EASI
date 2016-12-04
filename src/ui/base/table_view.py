# coding=utf-8

import abc

from src.low.custom_logging import make_logger
from src.qt import Qt, QTableView, QSortFilterProxyModel, QHeaderView, QBoxLayout
from src.ui.abstract.itable_view import ITableView, ITableViewRow, QModelIndex, QVariant, QAbstractTableModel
from src.ui.base.with_dyn_btns import WithDynamicButtons


logger = make_logger(__name__)


class BaseTableView(ITableView, WithDynamicButtons):
    def __init__(
            self,
            qt_table_view: QTableView,
            sorting_enabled: bool = True,
            parent=None,
            btns_layout: QBoxLayout = None
    ):
        QAbstractTableModel.__init__(self, parent)
        WithDynamicButtons.__init__(self, btns_layout)
        self.__table_data = []
        self.__qt_table = qt_table_view

        self.qt_table.verticalHeader().hide()
        self.qt_table.horizontalHeader().show()
        self.qt_table.setSelectionMode(1)
        self.qt_table.setSelectionBehavior(1)

        if sorting_enabled:
            self.proxy = QSortFilterProxyModel(self.qt_table)
            self.proxy.setSourceModel(self)
            self.qt_table.setSortingEnabled(True)
            self.qt_table.setModel(self.proxy)
            self.proxy.sort(0, Qt.AscendingOrder)
        else:
            self.qt_table.setSortingEnabled(False)
            self.proxy = None
            self.qt_table.setModel(self)

        if self.reset_model_signals is not None:
            def reset_model(sender):
                logger.debug('model reset triggered by: {}'.format(sender))
                self.reset_model()

            self.reset_model_method = reset_model
            for sig in self.reset_model_signals:
                sig.connect(self.reset_model_method)
        else:
            self.reset_model_method = None

        self.connect_signals()

    def connect_signals(self):
        self.__qt_table.clicked.connect(self.on_click)
        self.__qt_table.doubleClicked.connect(self.on_double_click)
        self.__qt_table.showEvent = self.on_show
        self.__qt_table.hideEvent = self.on_hide

    @property
    def selected_row(self) -> object:
        return self.qt_table.selectedIndexes()[0].data(Qt.UserRole)

    def resize_columns(self):
        try:
            for x in range(len(self.table_headers)):
                self.qt_table.horizontalHeader().setSectionResizeMode(x, QHeaderView.ResizeToContents)
            self.qt_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        except RuntimeError:
            pass

    @property
    def qt_table(self) -> QTableView:
        return self.__qt_table

    def reset_model(self):
        self.beginResetModel()
        self.build_model()
        self.resize_columns()
        self.endResetModel()

    @abc.abstractmethod
    def build_model(self):
        """Populates the model using self.add_row"""

    def reset_table_data(self):
        self.__table_data = []

    @property
    def table_data(self) -> list:
        return self.__table_data

    def data(self, index: QModelIndex, role=None) -> QVariant:
        if not index.isValid():
            return QVariant()
        row = self.get_row(index.row())
        if role == Qt.DisplayRole:
            return row.display_role[index.column()]
        elif role == Qt.UserRole:
            # noinspection PyTypeChecker
            return row.user_role
        elif role == Qt.ForegroundRole:
            # noinspection PyTypeChecker
            return row.foreground_role

    def headerData(self, column: int, orientation: int, role=None) -> QVariant:
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.table_headers[column]

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.table_data)

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self.table_headers)

    def flags(self, index: QModelIndex):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled

    def get_row(self, row: int) -> ITableViewRow:
        return self.table_data[row]

    def add_row(self, row: ITableViewRow):
        self.beginInsertRows(QModelIndex(), len(self.__table_data), len(self.__table_data))
        self.__table_data.append(row)
        self.endInsertRows()
        self.resize_columns()

    def remove_row(self, row: int):
        del self.__table_data[row]

    def set_updates_enabled(self, value: bool):
        self.__qt_table.setUpdatesEnabled(value)
