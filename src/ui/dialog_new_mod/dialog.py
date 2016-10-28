# coding=utf-8

from src.mod.mod_draft import ModDraft
from src.mod.mod_category import ModTypes
from src.qt import QDialog, dialog_default_flags, QVBoxLayout, Qt, qt_resources, QIcon, QRegExp, QRegExpValidator, \
    QStandardItemModel, QDialogButtonBox
from src.ui.base.qdialog import BaseDialog
from src.ui.form_mod_metadata.form import FormModMetadata
from src.ui.widget_balloon.widget import WidgetBalloon
from src.mod.local_mod import LocalMod


class _NewModDialog(QDialog):
    def __init__(self, mod_draft: ModDraft, parent=None):
        QDialog.__init__(self, parent, flags=dialog_default_flags)
        self.mod_draft = mod_draft
        self.setWindowIcon(QIcon(qt_resources.app_ico))
        self.setWindowTitle('New mod')
        self.form = FormModMetadata(self)
        self.setLayout(QVBoxLayout(self))
        self.layout = self.layout()
        assert isinstance(self.layout, QVBoxLayout)
        self.button_box = QDialogButtonBox(self)
        self.setup_form()
        self.setup_button_box()
        self.layout.addWidget(self.form, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.button_box, alignment=Qt.AlignBottom)
        self.error_widget = None
        self.show()

        
    def show(self):
        self.set_ok_and_save_buttons(False)
        self.set_save_and_reset_buttons(False)
        self.load_data_from_meta()
        super(_NewModDialog, self).show()
        

    def setup_button_box(self):
        self.button_box.addButton(self.button_box.Reset)
        self.button_box.addButton(self.button_box.Save)
        self.button_box.addButton(self.button_box.Ok)
        self.button_box.addButton(self.button_box.Cancel)
        self.button_box.addButton(self.button_box.Help)  # TODO connect
        self.button_box.button(self.button_box.Ok).setText('Create')
        self.button_box.button(self.button_box.Reset).clicked.connect(self.load_data_from_meta)
        self.button_box.button(self.button_box.Save).clicked.connect(self.save_data_to_meta)
        self.button_box.button(self.button_box.Ok).clicked.connect(self.accept)
        self.button_box.button(self.button_box.Cancel).clicked.connect(self.reject)

    def accept(self):
        self.save_data_to_meta()
        super(_NewModDialog, self).accept()

    def load_data_from_meta(self):
        self.form.edit_mod_name.setText(self.mod_draft.name)
        self.form.text_desc.setText(self.mod_draft.description)
        if self.mod_draft.category:
            self.form.combo_category.setCurrentIndex(
                self.form.combo_category.findText(self.mod_draft.category, flags=Qt.MatchFixedString)
            )
        self.set_save_and_reset_buttons(False)
        self.validate()

    def save_data_to_meta(self):
        self.mod_draft.name = self.form.edit_mod_name.text()
        self.mod_draft.category = self.form.combo_category.currentText()
        self.mod_draft.description = self.form.text_desc.toPlainText()
        self.mod_draft.write()
        self.set_save_and_reset_buttons(False)

    def setup_form(self):
        self.form.combo_category.addItem('<please select the type of your mod>')
        for mod_type in ModTypes.enum_category_names():
            self.form.combo_category.addItem(mod_type)
        model = self.form.combo_category.model()
        assert isinstance(model, QStandardItemModel)
        model.itemFromIndex(model.index(0, 0)).setEnabled(False)
        self.form.label_uuid.setText(self.mod_draft.uuid)
        self.form.label_help_name.setText(
            'The name of your new mod needs to contain at least one string of 4 letters.')
        self.form.edit_mod_name.setValidator(
            QRegExpValidator(QRegExp('.*[a-zA-Z]{4,}.*'), self.form.edit_mod_name)
        )
        self.form.edit_mod_name.textChanged.connect(self.meta_changed)
        self.form.combo_category.currentIndexChanged.connect(self.meta_changed)
        self.form.text_desc.textChanged.connect(self.meta_changed)

    def meta_changed(self):
        if self.error_widget:
            self.error_widget.hide()
            self.error_widget = None
        if not LocalMod.mod_name_is_available(self.form.edit_mod_name.text(), self.mod_draft.uuid):
            self.set_save_and_reset_buttons(False)
            self.set_ok_and_save_buttons(False)
            self.error_widget = WidgetBalloon.error(self.form.edit_mod_name, 'You already have a Mod with that name.')
            return
        self.set_save_and_reset_buttons(
            any([
                self.mod_draft.name != self.form.edit_mod_name.text(),
                self.mod_draft.category != self.form.combo_category.currentText(),
                self.mod_draft.description != self.form.text_desc.toPlainText(),
            ])
        )
        self.validate()

    def validate(self):
        self.set_ok_and_save_buttons(
            all({
                self.form.edit_mod_name.hasAcceptableInput(),
                self.form.combo_category.currentIndex() != 0,
            })
        )

    def set_ok_and_save_buttons(self, value: bool):
        self.button_box.button(self.button_box.Ok).setEnabled(value)
        self.button_box.button(self.button_box.Cancel).setEnabled(value)

    def set_save_and_reset_buttons(self, value: bool):
        self.button_box.button(self.button_box.Reset).setEnabled(value)
        self.button_box.button(self.button_box.Save).setEnabled(value)


class NewModDialog(BaseDialog):
    def __init__(self, mod_draft: ModDraft, parent=None):
        BaseDialog.__init__(self, _NewModDialog(mod_draft, parent))

    @staticmethod
    def make(mod_draft: ModDraft, parent=None):
        dialog = NewModDialog(mod_draft, parent).qobj
        return dialog.exec() == dialog.Accepted
