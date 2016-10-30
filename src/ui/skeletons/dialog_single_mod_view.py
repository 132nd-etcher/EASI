# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\DEV\EASI\EASIv0.0.11\src\ui\skeletons\dialog_single_mod_view.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(829, 513)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.table = QtWidgets.QTableView(Dialog)
        self.table.setMidLineWidth(8)
        self.table.setSortingEnabled(True)
        self.table.setWordWrap(True)
        self.table.setObjectName("table")
        self.table.horizontalHeader().setSortIndicatorShown(True)
        self.table.verticalHeader().setSortIndicatorShown(False)
        self.horizontalLayout.addWidget(self.table)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.btn_accept = QtWidgets.QPushButton(Dialog)
        self.btn_accept.setEnabled(False)
        self.btn_accept.setObjectName("btn_accept")
        self.verticalLayout.addWidget(self.btn_accept)
        self.btn_reset = QtWidgets.QPushButton(Dialog)
        self.btn_reset.setEnabled(False)
        self.btn_reset.setObjectName("btn_reset")
        self.verticalLayout.addWidget(self.btn_reset)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.btn_open = QtWidgets.QPushButton(Dialog)
        self.btn_open.setObjectName("btn_open")
        self.verticalLayout.addWidget(self.btn_open)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem1)
        self.check_hide_unchanged = QtWidgets.QCheckBox(Dialog)
        self.check_hide_unchanged.setObjectName("check_hide_unchanged")
        self.verticalLayout.addWidget(self.check_hide_unchanged)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.btn_done = QtWidgets.QPushButton(Dialog)
        self.btn_done.setEnabled(True)
        self.btn_done.setObjectName("btn_done")
        self.verticalLayout.addWidget(self.btn_done)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.btn_accept.setText(_translate("Dialog", "Accept changes"))
        self.btn_reset.setText(_translate("Dialog", "Reject changes"))
        self.btn_open.setText(_translate("Dialog", "Open folder"))
        self.check_hide_unchanged.setText(_translate("Dialog", "Hide unchanged files"))
        self.btn_done.setText(_translate("Dialog", "Done"))

