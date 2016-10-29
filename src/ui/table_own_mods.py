# coding=utf-8

from blinker_herald import signals

from src.mod.local_mod import LocalMod
from src.qt import QAbstractTableModel, QTableView, QModelIndex, Qt, QVariant, QSortFilterProxyModel, QHeaderView


class OwnModModel(QAbstractTableModel):
    columns_map = ['name', 'category', 'version', 'dcs_version', 'has_changed', 'status']

    def __init__(self, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.__data = []

    def refresh_data(self):
        self.beginResetModel()
        for draft in LocalMod.drafts():
            self.__data.append(
                (draft, 'draft')
            )
        self.endResetModel()

    def data(self, index: QModelIndex, role=Qt.DisplayRole):
        if not index.isValid():
            return QVariant()
        if role == Qt.DisplayRole:
            return getattr(self.__data[index.row()][0], self.columns_map[index.column()])

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.__data)

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self.columns_map)

    def headerData(self, col, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(str(self.columns_map[col]).capitalize().replace('_', ' '))
        else:
            return super(OwnModModel, self).headerData(col, orientation, role)


class TableOwnMods:
    def __init__(self, main_ui):
        self.__table = None
        self.__model = None
        self.__proxy = None
        self.main_ui = main_ui

    @property
    def table(self) -> QTableView:
        return self.__table

    @table.setter
    def table(self, value: QTableView):
        self.__table = value

    @property
    def model(self) -> OwnModModel:
        return self.__model

    @model.setter
    def model(self, value: OwnModModel):
        self.__model = value

    @property
    def proxy(self) -> QSortFilterProxyModel:
        return self.__proxy

    @proxy.setter
    def proxy(self, value: QSortFilterProxyModel):
        self.__proxy = value

    def setup(self):
        self.table = self.main_ui.table_own_mods
        self.model = OwnModModel(self.main_ui)
        self.proxy = QSortFilterProxyModel(self.main_ui)
        self.proxy.setSourceModel(self.model)
        self.table.setModel(self.proxy)
        self.table.verticalHeader().hide()
        self.table.horizontalHeader().show()
        self.table.setSelectionMode(1)
        self.table.setSelectionBehavior(1)
        self.table.setSortingEnabled(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        # noinspection PyUnusedLocal
        def refresh_mod_list(sender, signal_emitter, *args, **kwargs):
            if sender == 'MainUi':
                self.model.refresh_data()
                self.table.resizeColumnsToContents()

        signals.post_show.connect(refresh_mod_list, weak=False)
