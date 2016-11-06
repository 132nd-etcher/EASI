# coding=utf-8


import semver

from src.dcs.dcs_installs import DCSInstalls, DCSInstall
# noinspection PyUnresolvedReferences
from src.meta_repo.local_meta_repo import LocalMetaRepo
from src.mod.mod import Mod
from src.mod.dcs_version import DCSVersion
from src.mod.mod_category import ModTypes
from src.qt import QWidget
from src.qt import Qt, QRegExp, QRegExpValidator, \
    QMenu, QAction
from src.ui.skeletons.form_mod_metadata import Ui_Form
from src.ui.widget_balloon.widget import WidgetBalloon


class ModMetadataWidget(QWidget, Ui_Form):
    def __init__(self, mod: Mod or None, parent=None):
        QWidget.__init__(self, parent, flags=Qt.Widget)
        self.setupUi(self)
        self.mod = mod
        self.error_widget = None

        def make_version_menu():

            def __version_bump(bump_func):
                print('bumping')
                try:
                    self.edit_version.setText(bump_func(self.edit_version.text()))
                except ValueError:
                    pass

            def version_increment_major():
                __version_bump(semver.bump_major)

            def version_increment_minor():
                __version_bump(semver.bump_minor)

            def version_increment_patch():
                __version_bump(semver.bump_patch)

            def version_increment_prerelease():
                __version_bump(semver.bump_prerelease)

            def version_increment_build():
                __version_bump(semver.bump_build)

            version_menu = {
                'menu': QMenu(self),
                'maj': (QAction('Major (breaking changes)', self), version_increment_major),
                'min': (QAction('Minor (new features)', self), version_increment_minor),
                'pat': (QAction('Patch (bug fix)', self), version_increment_patch),
                'pre': (QAction('Prerelease (testing)', self), version_increment_prerelease),
                'bui': (QAction('Build (increments)', self), version_increment_build),
            }
            for action in ['maj', 'min', 'pat', 'pre', 'bui']:
                version_menu['menu'].addAction(version_menu[action][0])
                version_menu[action][0].triggered.connect(version_menu[action][1])
            self.btn_increment_version.setMenu(version_menu['menu'])

        make_version_menu()

        def make_dcs_version_pull_menu():

            def __pull_dcs_version(_branch: DCSInstall):
                self.edit_dcs_version.setText(_branch.version)

            def pull_dcs_version_from_stable():
                __pull_dcs_version(DCSInstalls().stable)

            def pull_dcs_version_from_beta():
                __pull_dcs_version(DCSInstalls().beta)

            def pull_dcs_version_from_alpha():
                __pull_dcs_version(DCSInstalls().alpha)

            pull_dcs = {
                'menu': QMenu(self),
                'stable': (QAction('Stable', self), DCSInstalls().stable, pull_dcs_version_from_stable),
                'beta': (QAction('Open Beta', self), DCSInstalls().beta, pull_dcs_version_from_beta),
                'alpha': (QAction('Open Alpha', self), DCSInstalls().alpha, pull_dcs_version_from_alpha),
            }

            for branch in ['stable', 'beta', 'alpha']:
                dcs_install = pull_dcs[branch][1]
                if dcs_install.install_path is None:
                    continue
                pull_dcs['menu'].addAction(pull_dcs[branch][0])
                pull_dcs[branch][0].triggered.connect(pull_dcs[branch][2])
            self.btn_pull_dcs_version.setMenu(pull_dcs['menu'])

        make_dcs_version_pull_menu()

        self.combo_category.addItem('<select what type of mod this is>')
        for mod_type in ModTypes.enum_category_names():
            self.combo_category.addItem(mod_type)
        self.combo_category.model().itemFromIndex(self.combo_category.model().index(0, 0)).setEnabled(False)
        self.label_help_name.setText(
            'The name of your new mod must contain at least one string of 4 letters.')
        self.edit_mod_name.setValidator(
            QRegExpValidator(QRegExp('.*[a-zA-Z]{4,}.*'), self.edit_mod_name)
        )
        self.edit_mod_name.textChanged.connect(self.meta_changed)
        self.combo_category.currentIndexChanged.connect(self.meta_changed)
        self.text_desc.textChanged.connect(self.meta_changed)
        self.edit_version.textChanged.connect(self.meta_changed)
        self.edit_dcs_version.textChanged.connect(self.meta_changed)

        self.btn_save = self.buttonBox.button(self.buttonBox.Save)
        self.btn_reset = self.buttonBox.button(self.buttonBox.Reset)
        self.btn_help = self.buttonBox.button(self.buttonBox.Help)

        self.btn_save.clicked.connect(self.save_data_to_meta)
        self.btn_reset.clicked.connect(self.load_data_from_meta)

        if self.mod is None:
            self.btn_save.setText('Create')
            self.edit_uuid.setText('-- pending creation --')
            self.edit_mod_name.setFocus()
        else:
            self.edit_uuid.setText(self.mod.meta.uuid)

    def showEvent(self, event):
        self.load_data_from_meta()
        super(ModMetadataWidget, self).showEvent(event)

    def load_data_from_meta(self):
        if self.mod is not None:
            self.edit_mod_name.setText(self.mod.meta.name)
            self.text_desc.setText(self.mod.meta.description)
            self.edit_version.setText(self.mod.meta.version)
            self.edit_dcs_version.setText(self.mod.meta.dcs_version)
            self.combo_category.setCurrentIndex(
                self.combo_category.findText(self.mod.meta.category, flags=Qt.MatchFixedString)
            )
            self.edit_version.setText(self.mod.meta.version)
            self.meta_changed()
        else:
            self.edit_version.setText('0.0.1')

    def save_data_to_meta(self):
        if self.mod is None:
            self.parent().mod = self.parent().meta_repo.create_new_mod(self.edit_mod_name.text())
            self.edit_uuid.setText(self.mod.meta.uuid)
            self.btn_save.setText('Save')
        self.mod.meta.name = self.edit_mod_name.text()
        self.mod.meta.category = self.combo_category.currentText()
        self.mod.meta.description = self.text_desc.toPlainText()
        self.mod.meta.version = self.edit_version.text()
        self.mod.meta.dcs_version = self.edit_dcs_version.text()
        self.mod.meta.write()
        self.meta_changed()

    def meta_changed(self):
        if self.error_widget:
            self.error_widget.hide()
            self.error_widget = None
        if self.edit_mod_name.text():
            if not self.parent().meta_repo.mod_name_is_available(self.edit_mod_name.text(), self.mod):
                self.error_widget = WidgetBalloon.error(
                    self.edit_mod_name,
                    'There is another mod with the same name in this repository.')
                return
        if self.edit_version.text():
            try:
                semver.parse(self.edit_version.text())
            except ValueError:
                self.error_widget = WidgetBalloon.error(self.edit_version, 'This is not a valid semver.')
                return
        if self.edit_dcs_version.text():
            if not DCSVersion.is_valid(self.edit_dcs_version.text()):
                self.error_widget = WidgetBalloon.error(self.edit_dcs_version, 'Invalid value')
                return
        meta_is_valid = all({
            self.edit_mod_name.hasAcceptableInput(),
            self.combo_category.currentIndex() != 0,
            self.edit_version.text() != '',
        })
        if self.mod is not None:
            meta_changed = any([
                self.mod.meta.name != self.edit_mod_name.text(),
                self.mod.meta.category != self.combo_category.currentText(),
                self.mod.meta.description != self.text_desc.toPlainText(),
                self.mod.meta.version != self.edit_version.text(),
                self.mod.meta.dcs_version != self.edit_dcs_version.text(),
            ])
            self.btn_reset.setEnabled(meta_changed)
            self.btn_save.setEnabled(meta_changed and meta_is_valid)
        else:
            self.btn_save.setEnabled(meta_is_valid)
