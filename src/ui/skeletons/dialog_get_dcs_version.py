# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\DEV\EASI\EASIv0.0.11\src\ui\skeletons\dialog_get_dcs_version.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 168)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.edit = QtWidgets.QLineEdit(Dialog)
        self.edit.setClearButtonEnabled(True)
        self.edit.setObjectName("edit")
        self.verticalLayout.addWidget(self.edit)
        self.btn_pull = QtWidgets.QToolButton(Dialog)
        self.btn_pull.setMinimumSize(QtCore.QSize(80, 0))
        self.btn_pull.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.btn_pull.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.btn_pull.setAutoRaise(False)
        self.btn_pull.setArrowType(QtCore.Qt.DownArrow)
        self.btn_pull.setObjectName("btn_pull")
        self.verticalLayout.addWidget(self.btn_pull)
        self.label_help_1 = QtWidgets.QLabel(Dialog)
        self.label_help_1.setObjectName("label_help_1")
        self.verticalLayout.addWidget(self.label_help_1)
        self.label_help_2 = QtWidgets.QLabel(Dialog)
        self.label_help_2.setWordWrap(True)
        self.label_help_2.setObjectName("label_help_2")
        self.verticalLayout.addWidget(self.label_help_2)
        self.label_help_3 = QtWidgets.QLabel(Dialog)
        self.label_help_3.setObjectName("label_help_3")
        self.verticalLayout.addWidget(self.label_help_3)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "DCS version"))
        self.btn_pull.setText(_translate("Dialog", "Pull from ..."))
        self.label_help_1.setText(_translate("Dialog", "A \"*\" means \"this bit doesn\'t matter\"."))
        self.label_help_2.setText(_translate("Dialog", "A \"+\" sign at the end means \"this version and all newer\"."))
        self.label_help_3.setText(_translate("Dialog", "Partial versions like \"1.2.*\" or \"2+\" are accepted."))

