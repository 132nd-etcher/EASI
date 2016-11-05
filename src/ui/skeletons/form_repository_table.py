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
        self.btn_add = QtWidgets.QPushButton(Form)
        self.btn_add.setObjectName("btn_add")
        self.verticalLayout.addWidget(self.btn_add)
        self.btn_remove = QtWidgets.QPushButton(Form)
        self.btn_remove.setObjectName("btn_remove")
        self.verticalLayout.addWidget(self.btn_remove)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.btn_details = QtWidgets.QPushButton(Form)
        self.btn_details.setObjectName("btn_details")
        self.verticalLayout.addWidget(self.btn_details)
        self.btn_open_on_gh = QtWidgets.QPushButton(Form)
        self.btn_open_on_gh.setObjectName("btn_open_on_gh")
        self.verticalLayout.addWidget(self.btn_open_on_gh)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.btn_add.setText(_translate("Form", "Add"))
        self.btn_remove.setText(_translate("Form", "Remove"))
        self.btn_details.setText(_translate("Form", "Details"))
        self.btn_open_on_gh.setText(_translate("Form", "Open on Github"))

