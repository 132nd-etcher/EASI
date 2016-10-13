# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\DEV\EASI\EASIv0.0.11\src\ui\skeletons\wizard_newmod.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Wizard(object):
    def setupUi(self, Wizard):
        Wizard.setObjectName("Wizard")
        Wizard.resize(400, 300)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/ico/app.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Wizard.setWindowIcon(icon)
        Wizard.setSizeGripEnabled(True)
        Wizard.setModal(True)
        Wizard.setWizardStyle(QtWidgets.QWizard.ClassicStyle)
        self.page_welcome = QtWidgets.QWizardPage()
        self.page_welcome.setAcceptDrops(False)
        self.page_welcome.setToolTipDuration(0)
        self.page_welcome.setObjectName("page_welcome")
        Wizard.addPage(self.page_welcome)

        self.retranslateUi(Wizard)
        QtCore.QMetaObject.connectSlotsByName(Wizard)

    def retranslateUi(self, Wizard):
        _translate = QtCore.QCoreApplication.translate
        Wizard.setWindowTitle(_translate("Wizard", "New mod"))
        self.page_welcome.setTitle(_translate("Wizard", "Welcome"))

from src.ui.resources import qt_resource_rc
