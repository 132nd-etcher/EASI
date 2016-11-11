# coding=utf-8


from src.ui.skeletons.wizard_create_mod import Ui_Wizard
from src.ui.base.qdialog import BaseDialog
from src.qt import Qt, QWizard, QWizardPage, dialog_default_flags
from .page_gh_login import GHLoginPage
from .page_final import FinalPage
from src.rem.gh.gh_session import GHSession


class _ModCreationWizard(Ui_Wizard, QWizard):

    def __init__(self, parent=None):
        QWizard.__init__(self, parent, flags=dialog_default_flags)
        self.setupUi(self)
        if not GHSession().user:
            self.addPage(GHLoginPage(self))
        self.addPage(FinalPage(self))

    def exec(self):
        if super(_ModCreationWizard, self).exec() == self.Accepted:
            return {}
        else:
            return None


class ModCreationWizard(BaseDialog):

    def __init__(self, parent=None):
        BaseDialog.__init__(self, _ModCreationWizard(parent))

    @staticmethod
    def make(parent=None):
        return ModCreationWizard(parent).qobj.exec()
