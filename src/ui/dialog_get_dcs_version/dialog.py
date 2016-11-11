# coding=utf-8


from src.dcs.dcs_installs import DCSInstalls, DCSInstall
from src.mod.dcs_version import DCSVersion
from src.qt import Qt, qt_resources, QDialog, dialog_default_flags, QIcon, QMenu, QAction
from src.ui.base.qdialog import BaseDialog
from src.ui.base.with_balloons import WithBalloons
from src.ui.skeletons.dialog_get_dcs_version import Ui_Dialog


class _GetDcsVersionDialog(QDialog, Ui_Dialog, WithBalloons):
    def __init__(self, title: str, text: str, default: str = '', parent=None):
        QDialog.__init__(self, parent=parent, flags=dialog_default_flags)
        WithBalloons.__init__(self)
        self.setupUi(self)
        self.setWindowTitle(title)
        self.label.setText(text)
        self.setWindowIcon(QIcon(qt_resources.app_ico))
        self.setWindowModality(Qt.ApplicationModal)
        self.edit.setText(default)
        self.btn_ok = self.buttonBox.button(self.buttonBox.Ok)
        self.btn_ok.setEnabled(False)
        self.edit.textChanged.connect(self.validate)

        pull_dcs = {
            'menu': QMenu(self),
            'stable': (
                QAction('Stable', self),
                DCSInstalls().stable,
                lambda: self.__pull_dcs_version(DCSInstalls().stable)
            ),
            'beta': (
                QAction('Open Beta', self),
                DCSInstalls().beta,
                lambda: self.__pull_dcs_version(DCSInstalls().beta)
            ),
            'alpha': (
                QAction('Open Alpha', self),
                DCSInstalls().alpha,
                lambda: self.__pull_dcs_version(DCSInstalls().alpha)
            ),
        }

        for branch in ['stable', 'beta', 'alpha']:
            dcs_install = pull_dcs[branch][1]
            if dcs_install.install_path is None:
                continue
            pull_dcs['menu'].addAction(pull_dcs[branch][0])
            pull_dcs[branch][0].triggered.connect(pull_dcs[branch][2])
        self.btn_pull_dcs_version.setMenu(pull_dcs['menu'])

    def __pull_dcs_version(self, _branch: DCSInstall):
        self.edit_dcs_version.setText(_branch.version)

    def validate(self):
        self.remove_balloons()
        if not DCSVersion.is_valid(self.edit.text()):
            self.show_error_balloon('Invalid DCS version string', self.edit)
            self.btn_ok.setEnabled(False)
        else:
            self.btn_ok.setEnabled(True)

    def exec(self):
        if super(_GetDcsVersionDialog, self).exec() == self.Accepted:
            return self.edit.text()
        else:
            return None


class GetDcsVersionDialog(BaseDialog):
    def __init__(self, title: str, text: str, default: str = '', parent=None):
        BaseDialog.__init__(self, _GetDcsVersionDialog(title, text, default, parent))

    @staticmethod
    def make(title: str, text: str, default: str = '', parent=None):
        return GetDcsVersionDialog(title, text, default, parent).qobj.exec()
