# coding=utf-8


from src.ui.skeletons.wizard_create_mod import Ui_Wizard
from src.ui.base.qdialog import BaseDialog
from src.qt import Qt, QWizard, QWizardPage, dialog_default_flags
from .page_gh_login import GHLoginPage
from .page_final import FinalPage
from .page_select_meta_repo import SelectMetaRepoPage
from src.rem.gh.gh_session import GHSession
import webbrowser


class _ModCreationWizard(Ui_Wizard, QWizard):

    def __init__(self, parent=None, meta_repo_name=None):
        self.meta_repo_name = meta_repo_name
        QWizard.__init__(self, parent, flags=dialog_default_flags)
        self.setupUi(self)
        if not GHSession().user:
            self.addPage(GHLoginPage(self))
        self.addPage(SelectMetaRepoPage(self))
        self.addPage(FinalPage(self))
        self.btn_help = self.button(self.HelpButton)
        self.btn_help.clicked.connect(self.show_help)

    def initializePage(self, page_id):
        self.btn_help.setEnabled(not self.page(page_id).help_link is None)
        super(_ModCreationWizard, self).initializePage(page_id)

    def show_help(self):
        link = self.currentPage().help_link
        if link:
            webbrowser.open_new_tab(link)

    def exec(self):
        if super(_ModCreationWizard, self).exec() == self.Accepted:
            return {}
        else:
            return None


class ModCreationWizard(BaseDialog):

    def __init__(self, parent=None, meta_repo_name=None):
        BaseDialog.__init__(self, _ModCreationWizard(parent, meta_repo_name))

    @staticmethod
    def make(parent=None, meta_repo_name=None):
        return ModCreationWizard(parent, meta_repo_name).qobj.exec()
