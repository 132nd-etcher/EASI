# coding=utf-8
import os

from blinker_herald import signals

from src.cache.cache_event import CacheEvent
from src.ui.skeletons.form_mod_files_table import Ui_Form
from src.ui.base.qdialog import BaseDialog
from src.qt import Qt, QDialog, dialog_default_flags, QAbstractTableModel, QVariant, QSortFilterProxyModel
from src.mod.mod import Mod
from src.mod.mod_file import ModFile


class ModFilesModel(QAbstractTableModel):

    map = [
        ('File', 'rel_path'),
        ('Size', 'human_size'),
    ]

    def __init__(self, mod: Mod, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.__data = []
        self.mod = mod
        self.refresh_model()

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self.map)

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.__data)

    def refresh_model(self):
        self.beginResetModel()
        self.__data = list(self.mod.local_files)
        self.endResetModel()

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return QVariant()
        if role == Qt.DisplayRole:
            cache_file = self.__data[index.row()]
            assert isinstance(cache_file, ModFile)
            return str(getattr(cache_file, self.map[index.column()][1]))

    def headerData(self, col, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(str(self.map[col][0]))
        else:
            return super(ModFilesModel, self).headerData(col, orientation, role)


class _ModFilesDialog(QDialog, Ui_Form):

    def __init__(self, mod: Mod, parent=None):
        QDialog.__init__(self, parent, flags=dialog_default_flags)
        self.setupUi(self)
        self.mod = mod
        self.model = ModFilesModel(mod, self)
        self.proxy = QSortFilterProxyModel(self)
        self.proxy.setSourceModel(self.model)
        self.tableView.setModel(self.proxy)
        self.tableView.verticalHeader().hide()
        self.tableView.horizontalHeader().show()
        self.tableView.setSelectionMode(1)
        self.tableView.setSelectionBehavior(1)
        self.tableView.setSortingEnabled(True)
        self.resize(parent.width(), parent.height())
        self.btn_open.clicked.connect(self.open_in_explorer)

        # noinspection PyUnusedLocal
        def cache_signal_handler(sender, signal_emitter, event: CacheEvent):
            if str(event.src.abspath()).startswith(str(self.mod.local_folder.abspath())):
                self.refresh_model()

        self.cache_signal_handler = cache_signal_handler

    def refresh_model(self):
        self.tableView.setUpdatesEnabled(False)
        self.model.refresh_model()
        self.tableView.setUpdatesEnabled(True)

    def showEvent(self, event):
        self.setWindowTitle('Showing files for: {}'.format(self.mod.meta.name))
        signals.post_cache_changed_event.connect(self.cache_signal_handler, weak=False)
        self.refresh_model()
        super(_ModFilesDialog, self).showEvent(event)

    def hideEvent(self, event):
        signals.post_cache_changed_event.disconnect(self.cache_signal_handler)
        super(_ModFilesDialog, self).hideEvent(event)

    def open_in_explorer(self):
        os.startfile(str(self.mod.local_folder.abspath()))

class ModFilesDialog(BaseDialog):

    def __init__(self, mod: Mod, parent=None):
        BaseDialog.__init__(self, _ModFilesDialog(mod, parent))
