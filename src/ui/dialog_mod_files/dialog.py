# coding=utf-8


from src.ui.skeletons.form_mod_files_table import Ui_Form
from src.ui.base.qdialog import BaseDialog
from src.qt import Qt, QDialog, dialog_default_flags, QAbstractTableModel, QVariant
from src.mod.mod import Mod
from src.cache.cache_file import CacheFile


class ModFilesModel(QAbstractTableModel):

    map = [
        ('Name', 'name')
    ]

    def __init__(self, mod: Mod, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.__data = []
        self.mod = mod
        self.refresh_model()

    def columnCount(self, parent=None, *args, **kwargs):
        return 1

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
            assert isinstance(cache_file, CacheFile)
            return getattr(cache_file, self.map[index.column()][1])

    def headerData(self, col, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(str(self.map[col][1]))
        else:
            return super(ModFilesModel, self).headerData(col, orientation, role)


class _ModFilesDialog(QDialog, Ui_Form):

    def __init__(self, mod: Mod, parent=None):
        QDialog.__init__(self, parent, flags=dialog_default_flags)
        self.setupUi(self)
        self.model = ModFilesModel(mod, self)
        self.tableView.setModel(self.model)
        self.tableView.verticalHeader().hide()
        self.tableView.horizontalHeader().show()
        self.tableView.setSelectionMode(1)
        self.tableView.setSelectionBehavior(1)
        self.tableView.setSortingEnabled(True)
        self.resize(parent.width(), parent.height())


class ModFilesDialog(BaseDialog):

    def __init__(self, mod: Mod, parent=None):
        BaseDialog.__init__(self, _ModFilesDialog(mod, parent))
