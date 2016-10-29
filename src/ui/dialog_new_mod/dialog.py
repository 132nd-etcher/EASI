# coding=utf-8

import semver

from src.dcs.dcs_installs import DCSInstalls, DCSInstall
from src.mod.local_mod import LocalMod
from src.mod.mod_category import ModTypes
from src.mod.mod_objects.mod_draft import ModDraft
from src.qt import QDialog, dialog_default_flags, QVBoxLayout, Qt, qt_resources, QIcon, QRegExp, QRegExpValidator, \
    QStandardItemModel, QDialogButtonBox, QMenu, QAction
from src.ui.base.qdialog import BaseDialog
from src.ui.form_mod_metadata.form import FormModMetadata
from src.ui.widget_balloon.widget import WidgetBalloon
from src.mod.dcs_version import DCSVersion


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
        self.version_menu = {
            'menu': QMenu(self),
            'maj': (QAction('Major (breaking changes)', self), self.version_increment_major),
            'min': (QAction('Minor (new features)', self), self.version_increment_minor),
            'pat': (QAction('Patch (bug fix)', self), self.version_increment_patch),
            'pre': (QAction('Prerelease (testing)', self), self.version_increment_prerelease),
        }
        for action in ['maj', 'min', 'pat', 'pre']:
            self.version_menu['menu'].addAction(self.version_menu[action][0])
            self.version_menu[action][0].triggered.connect(self.version_menu[action][1])
        self.form.btn_increment_version.setMenu(self.version_menu['menu'])
        self.pull_dcs = {
            'menu': QMenu(self),
            'stable': (QAction('Stable', self), DCSInstalls().stable, self.pull_dcs_version_from_stable),
            'beta': (QAction('Open Beta', self), DCSInstalls().beta, self.pull_dcs_version_from_beta),
            'alpha': (QAction('Open Alpha', self), DCSInstalls().alpha, self.pull_dcs_version_from_alpha),
        }
        for branch in ['stable', 'beta', 'alpha']:
            dcs_install = self.pull_dcs[branch][1]
            if dcs_install.install_path is None:
                continue
            self.pull_dcs['menu'].addAction(self.pull_dcs[branch][0])
            self.pull_dcs[branch][0].triggered.connect(self.pull_dcs[branch][2])
        self.form.btn_pull_dcs_version.setMenu(self.pull_dcs['menu'])
        self.show()

    def __version_bump(self, bump_func):
        try:
            self.form.edit_version.setText(bump_func(self.form.edit_version.text()))
        except ValueError:
            pass

    def version_increment_major(self):
        self.__version_bump(semver.bump_major)

    def version_increment_minor(self):
        self.__version_bump(semver.bump_minor)

    def version_increment_patch(self):
        self.__version_bump(semver.bump_patch)

    def version_increment_prerelease(self):
        self.__version_bump(semver.bump_prerelease)

    def __pull_dcs_version(self, branch: DCSInstall):
        self.form.edit_dcs_version.setText(branch.version)

    def pull_dcs_version_from_stable(self):
        self.__pull_dcs_version(DCSInstalls().stable)

    def pull_dcs_version_from_beta(self):
        self.__pull_dcs_version(DCSInstalls().beta)

    def pull_dcs_version_from_alpha(self):
        self.__pull_dcs_version(DCSInstalls().alpha)

    def show(self):
        self.set_ok_and_save_buttons(False)
        self.set_save_and_reset_buttons(False)
        self.load_data_from_meta()
        super(_NewModDialog, self).show()

    def setup_form(self):
        self.form.combo_category.addItem('<please select the type of your mod>')
        for mod_type in ModTypes.enum_category_names():
            self.form.combo_category.addItem(mod_type)
        model = self.form.combo_category.model()
        assert isinstance(model, QStandardItemModel)
        model.itemFromIndex(model.index(0, 0)).setEnabled(False)
        self.form.label_uuid.setText(self.mod_draft.uuid)
        self.form.label_help_name.setText(
            'The name of your new mod must contain at least one string of 4 letters.')
        self.form.edit_mod_name.setValidator(
            QRegExpValidator(QRegExp('.*[a-zA-Z]{4,}.*'), self.form.edit_mod_name)
        )
        self.form.edit_mod_name.textChanged.connect(self.meta_changed)
        self.form.combo_category.currentIndexChanged.connect(self.meta_changed)
        self.form.text_desc.textChanged.connect(self.meta_changed)
        self.form.edit_version.textChanged.connect(self.meta_changed)
        self.form.edit_dcs_version.textChanged.connect(self.meta_changed)

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
        self.form.edit_version.setText(self.mod_draft.version)
        self.form.edit_dcs_version.setText(self.mod_draft.dcs_version)
        if self.mod_draft.category:
            self.form.combo_category.setCurrentIndex(
                self.form.combo_category.findText(self.mod_draft.category, flags=Qt.MatchFixedString)
            )
        if self.mod_draft.version is None:
            self.form.edit_version.setText('0.0.1')
        else:
            self.form.edit_version.setText(self.mod_draft.version)
        self.set_save_and_reset_buttons(False)
        self.validate()

    def save_data_to_meta(self):
        self.mod_draft.name = self.form.edit_mod_name.text()
        self.mod_draft.category = self.form.combo_category.currentText()
        self.mod_draft.description = self.form.text_desc.toPlainText()
        self.mod_draft.version = self.form.edit_version.text()
        self.mod_draft.dcs_version = self.form.edit_dcs_version.text()
        self.mod_draft.write()
        self.set_save_and_reset_buttons(False)

    def meta_changed(self):
        if self.error_widget:
            self.error_widget.hide()
            self.error_widget = None
        if self.form.edit_mod_name.text():
            if not LocalMod.mod_name_is_available(self.form.edit_mod_name.text(), self.mod_draft.uuid):
                # self.set_save_and_reset_buttons(False)
                # self.set_ok_and_save_buttons(False)
                # self.error_widget = WidgetBalloon.error(self.form.edit_mod_name, 'You already have a Mod with that name.')
                self.validation_error(self.form.edit_mod_name, 'You already have a Mod with that name.')
                return
        if self.form.edit_version.text():
            try:
                semver.parse(self.form.edit_version.text())
            except ValueError:
                # self.set_save_and_reset_buttons(False)
                # self.set_ok_and_save_buttons(False)
                # self.error_widget = WidgetBalloon.error(self.form.edit_version, 'This is not a valid semver.')
                self.validation_error(self.form.edit_version, 'This is not a valid semver.')
                return
        if self.form.edit_dcs_version.text():
            if not DCSVersion.is_valid(self.form.edit_dcs_version.text()):
                self.validation_error(self.form.edit_dcs_version, 'Invalid value')
                return
        self.set_save_and_reset_buttons(
            any([
                self.mod_draft.name != self.form.edit_mod_name.text(),
                self.mod_draft.category != self.form.combo_category.currentText(),
                self.mod_draft.description != self.form.text_desc.toPlainText(),
                self.mod_draft.version != self.form.edit_version.text(),
                self.mod_draft.dcs_version != self.form.edit_dcs_version.text(),
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

    def validation_error(self, widget, msg):
        self.error_widget = WidgetBalloon.error(widget, msg)
        self.set_save_and_reset_buttons(False)
        self.set_ok_and_save_buttons(False)


class NewModDialog(BaseDialog):
    def __init__(self, mod_draft: ModDraft, parent=None):
        BaseDialog.__init__(self, _NewModDialog(mod_draft, parent))

    @staticmethod
    def make(mod_draft: ModDraft, parent=None):
        dialog = NewModDialog(mod_draft, parent).qobj
        return dialog.exec() == dialog.Accepted
