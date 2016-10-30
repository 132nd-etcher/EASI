# coding=utf-8

import semver

from src.dcs.dcs_installs import DCSInstalls, DCSInstall
from src.mod.dcs_version import DCSVersion
from src.mod.local_mod import LocalMod
from src.mod.mod_category import ModTypes
from src.mod.mod_objects.mod_base import BaseMod
from src.qt import QWidget
from src.qt import Qt, QRegExp, QRegExpValidator, \
    QStandardItemModel, QMenu, QAction, pyqtSignal
from src.ui.skeletons.form_mod_metadata import Ui_Form
from src.ui.widget_balloon.widget import WidgetBalloon
from src.cache.cache import Cache


class FormModMetadata(Ui_Form, QWidget):
    # first bool if meta is different, second if it is valid
    meta_has_changed = pyqtSignal(bool, bool, name='meta_has_changed')

    def __init__(self, mod: BaseMod, parent):
        QWidget.__init__(self, parent, flags=Qt.Widget)
        self.setupUi(self)
        self.error_widget = None
        self.__mod = None
        self.mod = mod
        self.version_menu = {
            'menu': QMenu(self),
            'maj': (QAction('Major (breaking changes)', self), self.version_increment_major),
            'min': (QAction('Minor (new features)', self), self.version_increment_minor),
            'pat': (QAction('Patch (bug fix)', self), self.version_increment_patch),
            'pre': (QAction('Prerelease (testing)', self), self.version_increment_prerelease),
            'bui': (QAction('Build (increments)', self), self.version_increment_build),
        }
        for action in ['maj', 'min', 'pat', 'pre', 'bui']:
            self.version_menu['menu'].addAction(self.version_menu[action][0])
            self.version_menu[action][0].triggered.connect(self.version_menu[action][1])
        self.btn_increment_version.setMenu(self.version_menu['menu'])
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
        self.btn_pull_dcs_version.setMenu(self.pull_dcs['menu'])

    @property
    def mod(self) -> BaseMod:
        return self.__mod

    @mod.setter
    def mod(self, value: BaseMod):
        self.__mod = value

    def __version_bump(self, bump_func):
        try:
            self.edit_version.setText(bump_func(self.edit_version.text()))
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

    def version_increment_build(self):
        self.__version_bump(semver.bump_build)

    def __pull_dcs_version(self, branch: DCSInstall):
        self.edit_dcs_version.setText(branch.version)

    def pull_dcs_version_from_stable(self):
        self.__pull_dcs_version(DCSInstalls().stable)

    def pull_dcs_version_from_beta(self):
        self.__pull_dcs_version(DCSInstalls().beta)

    def pull_dcs_version_from_alpha(self):
        self.__pull_dcs_version(DCSInstalls().alpha)

    def validation_error(self, widget, msg):
        self.error_widget = WidgetBalloon.error(widget, msg)
        self.meta_has_changed.emit(True, False)

    def setup(self):
        self.combo_category.addItem('<please select the type of your mod>')
        for mod_type in ModTypes.enum_category_names():
            self.combo_category.addItem(mod_type)
        model = self.combo_category.model()
        assert isinstance(model, QStandardItemModel)
        model.itemFromIndex(model.index(0, 0)).setEnabled(False)
        self.label_uuid.setText(self.mod.uuid)
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

    def meta_changed(self):
        if self.error_widget:
            self.error_widget.hide()
            self.error_widget = None
        if self.edit_mod_name.text():
            if not LocalMod.mod_name_is_available(self.edit_mod_name.text(), self.mod.uuid):
                self.validation_error(self.edit_mod_name, 'You already have another mod with that name.')
                return
        if self.edit_version.text():
            try:
                semver.parse(self.edit_version.text())
            except ValueError:
                self.validation_error(self.edit_version, 'This is not a valid semver.')
                return
        if self.edit_dcs_version.text():
            if not DCSVersion.is_valid(self.edit_dcs_version.text()):
                self.validation_error(self.edit_dcs_version, 'Invalid value')
                return

        different = any([
            self.mod.name != self.edit_mod_name.text(),
            self.mod.category != self.combo_category.currentText(),
            self.mod.description != self.text_desc.toPlainText(),
            self.mod.version != self.edit_version.text(),
            self.mod.dcs_version != self.edit_dcs_version.text(),
        ])

        valid = all({
            self.edit_mod_name.hasAcceptableInput(),
            self.combo_category.currentIndex() != 0,
            self.edit_version.text() != '',
        })
        self.meta_has_changed.emit(different, valid)

    def load_data_from_meta(self):
        self.edit_mod_name.setText(self.mod.name)
        self.text_desc.setText(self.mod.description)
        self.edit_version.setText(self.mod.version)
        self.edit_dcs_version.setText(self.mod.dcs_version)
        if self.mod.category:
            self.combo_category.setCurrentIndex(
                self.combo_category.findText(self.mod.category, flags=Qt.MatchFixedString)
            )
        if self.mod.version == '':
            self.edit_version.setText('0.0.1')
        else:
            self.edit_version.setText(self.mod.version)
        self.meta_changed()

    def save_data_to_meta(self):
        self.mod.name = self.edit_mod_name.text()
        self.mod.category = self.combo_category.currentText()
        self.mod.description = self.text_desc.toPlainText()
        self.mod.version = self.edit_version.text()
        self.mod.dcs_version = self.edit_dcs_version.text()
        self.mod.path = Cache().own_mods_folder.joinpath('{}.easi_mod_draft'.format(self.edit_mod_name.text()))
        self.mod.write()
        self.meta_has_changed.emit(False, True)
