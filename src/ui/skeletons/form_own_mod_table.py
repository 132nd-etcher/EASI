# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\DEV\EASI\EASIv0.0.11\src\ui\skeletons\form_own_mod_table.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(830, 541)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.combo_repo = QtWidgets.QComboBox(self.groupBox)
        self.combo_repo.setObjectName("combo_repo")
        self.verticalLayout_3.addWidget(self.combo_repo)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.table = QtWidgets.QTableView(self.groupBox_2)
        self.table.setObjectName("table")
        self.horizontalLayout.addWidget(self.table)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.btn_create_mod = QtWidgets.QPushButton(self.groupBox_2)
        self.btn_create_mod.setObjectName("btn_create_mod")
        self.verticalLayout.addWidget(self.btn_create_mod)
        self.btn_details = QtWidgets.QPushButton(self.groupBox_2)
        self.btn_details.setObjectName("btn_details")
        self.verticalLayout.addWidget(self.btn_details)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.btn_trash_mod = QtWidgets.QPushButton(self.groupBox_2)
        self.btn_trash_mod.setObjectName("btn_trash_mod")
        self.verticalLayout.addWidget(self.btn_trash_mod)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2.addWidget(self.groupBox_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox.setTitle(_translate("Form", "Repository"))
        self.groupBox_2.setTitle(_translate("Form", "Mods"))
        self.btn_create_mod.setText(_translate("Form", "Create new mod"))
        self.btn_details.setText(_translate("Form", "Details"))
        self.btn_trash_mod.setText(_translate("Form", "Remove mod"))

