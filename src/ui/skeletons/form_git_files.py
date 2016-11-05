# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\DEV\EASI\EASIv0.0.11\src\ui\skeletons\form_git_files.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(742, 500)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.table = QtWidgets.QTableView(Form)
        self.table.setMidLineWidth(8)
        self.table.setSortingEnabled(True)
        self.table.setWordWrap(True)
        self.table.setObjectName("table")
        self.table.horizontalHeader().setSortIndicatorShown(True)
        self.table.verticalHeader().setSortIndicatorShown(False)
        self.horizontalLayout.addWidget(self.table)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.btn_accept = QtWidgets.QPushButton(Form)
        self.btn_accept.setEnabled(False)
        self.btn_accept.setObjectName("btn_accept")
        self.verticalLayout.addWidget(self.btn_accept)
        self.btn_reset = QtWidgets.QPushButton(Form)
        self.btn_reset.setEnabled(False)
        self.btn_reset.setObjectName("btn_reset")
        self.verticalLayout.addWidget(self.btn_reset)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.btn_open = QtWidgets.QPushButton(Form)
        self.btn_open.setObjectName("btn_open")
        self.verticalLayout.addWidget(self.btn_open)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem1)
        self.check_show_unchanged = QtWidgets.QCheckBox(Form)
        self.check_show_unchanged.setChecked(False)
        self.check_show_unchanged.setObjectName("check_show_unchanged")
        self.verticalLayout.addWidget(self.check_show_unchanged)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.btn_accept.setText(_translate("Form", "Accept changes"))
        self.btn_reset.setText(_translate("Form", "Reject changes"))
        self.btn_open.setText(_translate("Form", "Open folder"))
        self.check_show_unchanged.setText(_translate("Form", "Show unchanged files"))

