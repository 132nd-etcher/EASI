# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\DEV\EASI\EASIv0.0.11\src\ui\skeletons\form_repository_table.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(830, 541)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.table = QtWidgets.QTableView(Form)
        self.table.setObjectName("table")
        self.horizontalLayout.addWidget(self.table)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.btn_create_mod = QtWidgets.QPushButton(Form)
        self.btn_create_mod.setObjectName("btn_create_mod")
        self.verticalLayout.addWidget(self.btn_create_mod)
        self.btn_details = QtWidgets.QPushButton(Form)
        self.btn_details.setObjectName("btn_details")
        self.verticalLayout.addWidget(self.btn_details)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.btn_trash_mod = QtWidgets.QPushButton(Form)
        self.btn_trash_mod.setObjectName("btn_trash_mod")
        self.verticalLayout.addWidget(self.btn_trash_mod)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.btn_create_mod.setText(_translate("Form", "Create new mod"))
        self.btn_details.setText(_translate("Form", "Details"))
        self.btn_trash_mod.setText(_translate("Form", "Remove mod"))

