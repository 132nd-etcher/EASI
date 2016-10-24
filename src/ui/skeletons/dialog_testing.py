# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\DEV\EASI\EASIv0.0.11\src\ui\skeletons\dialog_testing.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(817, 587)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.btn_make_msgbox = QtWidgets.QPushButton(Dialog)
        self.btn_make_msgbox.setObjectName("btn_make_msgbox")
        self.verticalLayout.addWidget(self.btn_make_msgbox)
        self.btn_make_progress = QtWidgets.QPushButton(Dialog)
        self.btn_make_progress.setObjectName("btn_make_progress")
        self.verticalLayout.addWidget(self.btn_make_progress)
        self.btn_make_dual_progress = QtWidgets.QPushButton(Dialog)
        self.btn_make_dual_progress.setObjectName("btn_make_dual_progress")
        self.verticalLayout.addWidget(self.btn_make_dual_progress)
        self.btn_make_confirm = QtWidgets.QPushButton(Dialog)
        self.btn_make_confirm.setObjectName("btn_make_confirm")
        self.verticalLayout.addWidget(self.btn_make_confirm)
        self.btn_make_input_dialog = QtWidgets.QPushButton(Dialog)
        self.btn_make_input_dialog.setObjectName("btn_make_input_dialog")
        self.verticalLayout.addWidget(self.btn_make_input_dialog)
        self.btn_test_logger = QtWidgets.QPushButton(Dialog)
        self.btn_test_logger.setObjectName("btn_test_logger")
        self.verticalLayout.addWidget(self.btn_test_logger)
        self.textBrowser = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser.setAcceptDrops(False)
        self.textBrowser.setAcceptRichText(True)
        self.textBrowser.setOpenExternalLinks(True)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.btn_make_msgbox.setText(_translate("Dialog", "Make msgbox"))
        self.btn_make_progress.setText(_translate("Dialog", "Make progress"))
        self.btn_make_dual_progress.setText(_translate("Dialog", "Make dual progress"))
        self.btn_make_confirm.setText(_translate("Dialog", "Make confirm dialog"))
        self.btn_make_input_dialog.setText(_translate("Dialog", "Make input dialog"))
        self.btn_test_logger.setText(_translate("Dialog", "Test Qt Logger"))

