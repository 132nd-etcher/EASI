# coding=utf-8


from src.git.local_meta_repo import LocalMetaRepo
from src.mod.local_mod import LocalMod
from src.mod.mod import Mod
from src.qt import QWidget, Qt
from src.ui.dialog_confirm.dialog import ConfirmDialog
from src.ui.skeletons.form_mod_remote import Ui_Form


class ModRemoteWidget(Ui_Form, QWidget):
    def __init__(self, mod: Mod, parent=None):
        QWidget.__init__(self, parent, flags=Qt.Widget)
        self.setupUi(self)
        self.combo_meta.addItems(LocalMetaRepo().repo_names())
        self.__mod = mod
        self.set_combo_meta_to_mod_value()
        self.combo_meta.currentIndexChanged.connect(self.change_meta_repository)

    def set_combo_meta_to_mod_value(self):
        if self.mod is not None:
            print('caribou',
                self.combo_meta.findText(self.mod.meta.meta_repo_name, Qt.MatchExactly))
            self.combo_meta.setCurrentIndex(
                self.combo_meta.findText(self.mod.meta.meta_repo_name, Qt.MatchExactly)
            )

    def change_meta_repository(self):
        if self.mod.meta.meta_repo_name != self.combo_meta.currentText():
            if ConfirmDialog.make(
                    question='Are you sure you want to move this mod from "{}" to "{}" ?'.format(
                        self.mod.meta.meta_repo_name, self.combo_meta.currentText()),
                    parent=self.parent()):
                LocalMod().move_meta(self.mod.meta.name, self.combo_meta.currentText())
            else:
                self.set_combo_meta_to_mod_value()

    @property
    def mod(self) -> Mod:
        return self.__mod

    @mod.setter
    def mod(self, value: Mod):
        self.__mod = value
        self.set_combo_meta_to_mod_value()
