# coding=utf-8
import os
from collections import OrderedDict

from blinker_herald import signals

from src.cache.cache_event import CacheEvent
from src.mod.mod import Mod
from src.mod.mod_file import ModFile
from src.qt import Qt, QDialog, dialog_default_flags, QAbstractTableModel, QVariant, QSortFilterProxyModel, \
    QModelIndex, QHeaderView, QColor, \
    QTimer, pyqtSignal
from src.ui.base.qdialog import BaseDialog
from src.ui.skeletons.form_mod_files_table import Ui_Form
from src.sig import SigProgress
from src.threadpool.threadpool import ThreadPool


class ModFilesModel(QAbstractTableModel):
    map = [
        ('File', 'rel_path', Qt.ItemIsEnabled),
        ('Size', 'human_size', Qt.ItemIsEnabled),
        ('Last changed', 'last_changed', Qt.ItemIsEnabled),
        ('Operation', 'action', Qt.ItemIsEnabled),
        ('Status', 'status', Qt.ItemIsEnabled),
    ]

    def __init__(self, mod: Mod, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.__data = []
        self.mod = mod

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self.map)

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.__data)

    def refresh_model(self):
        self.beginResetModel()
        self.__data = []
        mod_meta = OrderedDict(self.mod.meta.files)
        local_files = list(self.mod.local_files)
        if local_files:
            SigProgress().show('Reading local files...', '')
        count = 0
        for mod_file in local_files:
            SigProgress().set_progress_text('Reading file: {}'.format(mod_file.rel_path))
            color = QColor(Qt.black)
            status = 'unchanged'
            if mod_file.rel_path in mod_meta:
                if mod_file.meta != mod_meta[mod_file.rel_path]:
                    print(mod_file.meta)
                    print(mod_meta[mod_file.rel_path])
                    color = QColor(Qt.blue)
                    status = 'updated'
                del mod_meta[mod_file.rel_path]
            else:
                color = QColor(Qt.darkGreen)
                status = 'new'
            if mod_file.cache_file.isdir:
                values = ['{}\\'.format(mod_file.rel_path)] + [''] * (len(self.map) - 1)
                color = QColor(Qt.gray)
                values.append('directory')
            else:
                values = [str(getattr(mod_file, attr[1])) for attr in self.map if attr[1] not in ['status']]
                values.append(status)
            self.__data.append(
                (values, mod_file, color)
            )
            count += 1
            SigProgress().set_progress((count / len(local_files) * 100))
        if len(mod_meta) > 0:
            SigProgress().show('Adding removed files...', '')
        count = 0
        for rel_path in mod_meta:
            SigProgress().set_progress_text('Adding  removed file: {}'.format(rel_path))
            values = [str(mod_meta[rel_path].get(attr[1], '')) for attr in self.map if attr[1] not in ['status']]
            values.append('deleted')
            self.__data.append(
                (values, None, QColor(Qt.red))
            )
            count += 1
            SigProgress().set_progress((count / len(mod_meta) * 100))
        self.endResetModel()

    def data(self, index: QModelIndex, role=Qt.DisplayRole):
        if not index.isValid():
            return QVariant()
        if role == Qt.DisplayRole:
            return self.__data[index.row()][0][index.column()]
        elif role == Qt.UserRole:
            return self.__data[index.row()][1]
        elif role == Qt.TextColorRole:
            return self.__data[index.row()][2]

    def headerData(self, col, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(str(self.map[col][0]))
        else:
            return super(ModFilesModel, self).headerData(col, orientation, role)

    def flags(self, index: QModelIndex):
        if not index.isValid():
            return Qt.ItemIsEnabled
        return self.map[index.column()][2]


class _ModFilesDialog(QDialog, Ui_Form):
    sig_refresh = pyqtSignal(name='refresh')

    def __init__(self, mod: Mod, parent=None):
        QDialog.__init__(self, parent, flags=dialog_default_flags)
        self.setupUi(self)
        self.pool = ThreadPool(1, 'mod_files')
        self.resize(parent.width(), parent.height())
        self.mod = mod
        self.model = ModFilesModel(mod, self)
        self.proxy = QSortFilterProxyModel(self)
        self.proxy.setSourceModel(self.model)
        self.tableView.setModel(self.proxy)
        self.tableView.verticalHeader().hide()
        self.tableView.horizontalHeader().show()
        # self.tableView.setSelectionMode(3)
        # self.tableView.setSelectionBehavior(1)
        self.tableView.setSortingEnabled(True)
        self.btn_open.clicked.connect(self.open_in_explorer)
        self.btn_save.clicked.connect(self.save)
        self.btn_reset.clicked.connect(self.reset)
        self.refresh_scheduler = QTimer(self)
        # noinspection PyUnresolvedReferences
        self.refresh_scheduler.timeout.connect(self.refresh_model)
        self.sig_refresh.connect(self.start_timer)

        # noinspection PyUnusedLocal
        def cache_signal_handler(sender, signal_emitter, event: CacheEvent):
            if str(event.src.abspath()).startswith(str(self.mod.local_folder.abspath())):
                self.sig_refresh.emit()

        self.cache_signal_handler = cache_signal_handler
        self.tableView.doubleClicked.connect(self.on_double_click)

    def selected_mod_file(self, index: QModelIndex) -> ModFile:
        return self.model.data(self.model.createIndex(self.proxy.mapToSource(index).row(), 0), role=Qt.UserRole)

    def on_double_click(self, index: QModelIndex):
        mod_file = self.selected_mod_file(index)
        if mod_file:
            os.startfile(mod_file.abspath)

        # print(self.selected_mod_file)
        # os.startfile(self.selected_mod_file.abspath)

    def start_timer(self):
        self.refresh_scheduler.start(500)

    def resize_columns(self):
        for x in range(len(self.model.map)):
            self.tableView.horizontalHeader().setSectionResizeMode(x, QHeaderView.ResizeToContents)
        self.tableView.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

    def __refresh_model(self):
        self.refresh_scheduler.stop()
        self.tableView.setUpdatesEnabled(False)
        self.model.refresh_model()
        self.resize_columns()
        self.tableView.setUpdatesEnabled(True)

    def refresh_model(self):
        self.pool.queue_task(self.__refresh_model)

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

    def __save(self):
        self.tableView.setUpdatesEnabled(False)
        SigProgress().show('Saving metadata...', '')
        files = list(self.mod.local_files)
        current = 0
        d = OrderedDict()
        for mod_file in files:
            SigProgress().set_progress_text(mod_file.rel_path)
            d[str(mod_file.rel_path)] = mod_file.meta
            current += 1
            SigProgress().set_progress((current / len(files)) * 100)
        self.mod.meta.files = d
        self.mod.meta.write()
        self.tableView.setUpdatesEnabled(True)
        self.refresh_model()

    def save(self):
        self.pool.queue_task(self.__save)

    def reset(self):
        pass


class ModFilesDialog(BaseDialog):
    def __init__(self, mod: Mod, parent=None):
        BaseDialog.__init__(self, _ModFilesDialog(mod, parent))
