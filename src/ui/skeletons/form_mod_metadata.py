# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\DEV\EASI\EASIv0.0.11\src\ui\skeletons\form_mod_metadata.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 4, 0, 1, 1)
        self.edit_mod_name = QtWidgets.QLineEdit(Form)
        self.edit_mod_name.setObjectName("edit_mod_name")
        self.gridLayout_2.addWidget(self.edit_mod_name, 1, 1, 1, 1)
        self.label_uuid = QtWidgets.QLabel(Form)
        self.label_uuid.setObjectName("label_uuid")
        self.gridLayout_2.addWidget(self.label_uuid, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 1, 0, 1, 1)
        self.text_desc = QtWidgets.QTextBrowser(Form)
        self.text_desc.setReadOnly(False)
        self.text_desc.setObjectName("text_desc")
        self.gridLayout_2.addWidget(self.text_desc, 4, 1, 1, 1)
        self.combo_category = QtWidgets.QComboBox(Form)
        self.combo_category.setObjectName("combo_category")
        self.gridLayout_2.addWidget(self.combo_category, 3, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 3, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)
        self.label_help_name = QtWidgets.QLabel(Form)
        self.label_help_name.setObjectName("label_help_name")
        self.gridLayout_2.addWidget(self.label_help_name, 2, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_4.setText(_translate("Form", "Description"))
        self.label_uuid.setText(_translate("Form", "TextLabel"))
        self.label.setText(_translate("Form", "Name"))
        self.label_3.setText(_translate("Form", "Category"))
        self.label_2.setText(_translate("Form", "Unique ID"))
        self.label_help_name.setText(_translate("Form", "TextLabel"))

