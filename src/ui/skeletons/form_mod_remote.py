# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\DEV\EASI\EASIv0.0.11\src\ui\skeletons\form_mod_remote.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(628, 459)
        self.formLayout = QtWidgets.QFormLayout(Form)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.combo_meta = QtWidgets.QComboBox(Form)
        self.combo_meta.setObjectName("combo_meta")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.combo_meta)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.combo_files = QtWidgets.QComboBox(Form)
        self.combo_files.setObjectName("combo_files")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.combo_files)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.btn_status_refresh = QtWidgets.QToolButton(Form)
        self.btn_status_refresh.setObjectName("btn_status_refresh")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.btn_status_refresh)
        self.label_status = QtWidgets.QLabel(Form)
        self.label_status.setObjectName("label_status")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.label_status)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Meta repository"))
        self.label_2.setText(_translate("Form", "Hosting provider"))
        self.label_3.setText(_translate("Form", "Status:"))
        self.btn_status_refresh.setText(_translate("Form", "Refresh"))
        self.label_status.setText(_translate("Form", "TextLabel"))

