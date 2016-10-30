# coding=utf-8

import os
from src.mod.mod_objects.mod_draft import ModDraft
from src.mod.mod_objects.mod_base import BaseMod
from src.qt import QDialog, dialog_default_flags, QVBoxLayout, Qt, qt_resources, QIcon, QDialogButtonBox
from src.ui.base.qdialog import BaseDialog
from src.ui.form_mod_metadata.form import FormModMetadata


class _ModMetaDataDialog(QDialog):
    def __init__(self, title: str, ok_btn_text: str, mod: BaseMod, parent=None):
        QDialog.__init__(self, parent, flags=dialog_default_flags)
        self.mod_draft = BaseMod
        self.setWindowIcon(QIcon(qt_resources.app_ico))
        self.setWindowTitle(title)
        self.form = FormModMetadata(mod, self)
        self.setLayout(QVBoxLayout(self))
        self.layout = self.layout()
        assert isinstance(self.layout, QVBoxLayout)
        self.button_box = QDialogButtonBox(self)
        self.form.setup()
        self.button_box.addButton(self.button_box.Reset)
        self.button_box.addButton(self.button_box.Save)
        self.button_box.addButton(self.button_box.Ok)
        self.button_box.addButton(self.button_box.Cancel)
        self.button_box.addButton(self.button_box.Help)  # TODO connect
        self.button_box.button(self.button_box.Ok).setText(ok_btn_text)
        self.button_box.button(self.button_box.Reset).clicked.connect(self.form.load_data_from_meta)
        self.button_box.button(self.button_box.Save).clicked.connect(self.form.save_data_to_meta)
        self.button_box.button(self.button_box.Ok).clicked.connect(self.accept)
        self.button_box.button(self.button_box.Cancel).clicked.connect(self.reject)
        self.layout.addWidget(self.form, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.button_box, alignment=Qt.AlignBottom)
        self.form.meta_has_changed.connect(self.meta_has_changed)
        self.show()

    def show(self):
        self.form.load_data_from_meta()
        super(_ModMetaDataDialog, self).show()

    def accept(self):
        self.form.save_data_to_meta()
        super(_ModMetaDataDialog, self).accept()

    def meta_has_changed(self, different: bool, valid: bool):
        self.button_box.button(self.button_box.Reset).setEnabled(different)
        self.button_box.button(self.button_box.Ok).setEnabled(valid)
        self.button_box.button(self.button_box.Save).setEnabled(different and valid)


class NewModDialog(BaseDialog):
    def __init__(self, mod_draft: ModDraft, parent=None):
        BaseDialog.__init__(self, _ModMetaDataDialog('New mod', 'Create', mod_draft, parent))

    @property
    def qobj(self) -> _ModMetaDataDialog:
        return super(NewModDialog, self).qobj

    @staticmethod
    def make(mod_draft: ModDraft, parent=None):
        dialog = NewModDialog(mod_draft, parent).qobj
        result = dialog.exec() == dialog.Accepted
        if not result:
            try:
                os.remove(mod_draft.path)
            except FileNotFoundError:
                pass
        return result


class EditModDialog(BaseDialog):
    def __init__(self, mod: BaseMod, parent=None):
        BaseDialog.__init__(self, _ModMetaDataDialog('Mod metadata', 'Save and exit', mod, parent))

    @staticmethod
    def make(mod: BaseMod, parent=None):
        dialog = EditModDialog(mod, parent).qobj
        return dialog.exec() == dialog.Accepted
