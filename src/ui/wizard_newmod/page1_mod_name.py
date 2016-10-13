# coding=utf-8

from string import ascii_letters, digits
from src.qt import QWizardPage, QLabel, QLineEdit, QVBoxLayout, Qt, QFormLayout, QRegExpValidator, QRegExp
from src.ui.widget_balloon.widget import WidgetBalloon


class PageModName(QWizardPage):
    def __init__(self, title: str, parent=None):
        QWizardPage.__init__(self, parent)
        self.setTitle(title)
        self.setLayout(QVBoxLayout(self))
        self.intro = QLabel('Choose a name for your new mod.<br><br>'
                            'The name needs to contain at least one string of 4 letters.')
        self.edit_mod_name = QLineEdit(self)
        self.edit_mod_name.setValidator(
            QRegExpValidator(QRegExp('.*[a-zA-Z]{4,}.*'), self.edit_mod_name)
        )
        # noinspection PyUnresolvedReferences
        self.edit_mod_name.textChanged.connect(self.completeChanged)
        self.registerField('modname*',
                           self.edit_mod_name,
                           changedSignal=self.edit_mod_name.textChanged)
        self.form = QFormLayout(self)
        self.form.addRow('Mod name', self.edit_mod_name)
        self.layout().addWidget(self.intro, alignment=Qt.AlignLeft)
        self.layout().addSpacing(40)
        self.layout().addLayout(self.form)
        print(self.layout())

    def cleanupPage(self):
        self.edit_mod_name.setText('')
        super(PageModName, self).cleanupPage()

    def layout(self) -> QVBoxLayout:
        return super(PageModName, self).layout()
