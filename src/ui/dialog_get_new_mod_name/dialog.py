# coding=utf-8

from src.meta_repo.local_meta_repo import LocalMetaRepo
from src.qt import QDialog, Qt, dialog_default_flags, QLineEdit, QLabel, QDialogButtonBox, QVBoxLayout, \
    QRegExp, QRegExpValidator
from src.ui.base.qdialog import BaseDialog


class _NewModNameDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent, flags=dialog_default_flags)
        self.__layout = QVBoxLayout(self)
        self.setLayout(self.__layout)
        self.intro_label = QLabel('Choose a name for your mod:')
        self.__layout.addWidget(self.intro_label, alignment=Qt.AlignCenter)
        self.edit_name = QLineEdit()
        self.edit_name.setValidator(
            QRegExpValidator(QRegExp('.*[a-zA-Z]{4,}.*'), self.edit_name)
        )
        # noinspection PyUnresolvedReferences
        self.edit_name.textChanged.connect(self.on_mod_name_changed)
        self.__layout.addWidget(self.edit_name, alignment=Qt.AlignCenter)
        self.error_label = QLabel('The name of your new mod must contain at least one string of 4 letters.')
        self.__layout.addWidget(self.error_label, alignment=Qt.AlignCenter)
        self.button_box = QDialogButtonBox()
        self.button_box.addButton(QDialogButtonBox.Ok)
        self.btn_ok = self.button_box.button(QDialogButtonBox.Ok)
        self.button_box.addButton(QDialogButtonBox.Cancel)
        self.btn_cancel = self.button_box.button(QDialogButtonBox.Cancel)
        self.btn_ok.clicked.connect(self.btn_ok_clicked)
        self.btn_cancel.clicked.connect(self.btn_cancel_clicked)
        self.__layout.addWidget(self.button_box, alignment=Qt.AlignCenter)
        self.btn_ok.setEnabled(False)

    def on_mod_name_changed(self):
        if not self.edit_name.hasAcceptableInput():
            self.error_label.setText('The name of your new mod must contain at least one string of 4 letters.')
            self.btn_ok.setEnabled(False)
        elif self.new_mod_name in LocalMetaRepo().mod_names:
            self.error_label.setText('You already have a mod with that name.')
            self.btn_ok.setEnabled(False)
        else:
            self.error_label.setText('')
            self.btn_ok.setEnabled(True)

    def btn_ok_clicked(self):
        self.accept()

    def btn_cancel_clicked(self):
        self.reject()

    @property
    def new_mod_name(self):
        return self.edit_name.text()


class NewModNameDialog(BaseDialog):
    def __init__(self, parent=None):
        BaseDialog.__init__(self, _NewModNameDialog(parent))
        self.qobj.show()

    @property
    def qobj(self) -> _NewModNameDialog:
        return super(NewModNameDialog, self).qobj

    def exec(self):
        result = self.qobj.exec()
        if result == self.qobj.Rejected:
            return None
        else:
            return self.qobj.new_mod_name
