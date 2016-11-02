# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\DEV\EASI\EASIv0.0.11\src\ui\skeletons\form_own_mod_view.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(873, 582)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.layout_tabs = QtWidgets.QHBoxLayout()
        self.layout_tabs.setSpacing(0)
        self.layout_tabs.setObjectName("layout_tabs")
        self.btn_metadata = QtWidgets.QToolButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_metadata.sizePolicy().hasHeightForWidth())
        self.btn_metadata.setSizePolicy(sizePolicy)
        self.btn_metadata.setMinimumSize(QtCore.QSize(90, 30))
        self.btn_metadata.setCheckable(True)
        self.btn_metadata.setChecked(False)
        self.btn_metadata.setAutoExclusive(True)
        self.btn_metadata.setPopupMode(QtWidgets.QToolButton.DelayedPopup)
        self.btn_metadata.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.btn_metadata.setAutoRaise(True)
        self.btn_metadata.setObjectName("btn_metadata")
        self.layout_tabs.addWidget(self.btn_metadata)
        self.btn_local_files = QtWidgets.QToolButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_local_files.sizePolicy().hasHeightForWidth())
        self.btn_local_files.setSizePolicy(sizePolicy)
        self.btn_local_files.setMinimumSize(QtCore.QSize(90, 30))
        self.btn_local_files.setAutoFillBackground(False)
        self.btn_local_files.setCheckable(True)
        self.btn_local_files.setChecked(False)
        self.btn_local_files.setAutoExclusive(True)
        self.btn_local_files.setPopupMode(QtWidgets.QToolButton.DelayedPopup)
        self.btn_local_files.setAutoRaise(True)
        self.btn_local_files.setObjectName("btn_local_files")
        self.layout_tabs.addWidget(self.btn_local_files)
        self.verticalLayout.addLayout(self.layout_tabs)
        self.line = QtWidgets.QFrame(Form)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setObjectName("main_layout")
        self.verticalLayout.addLayout(self.main_layout)
        self.verticalLayout.setStretch(2, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.btn_metadata.setText(_translate("Form", "Metadata"))
        self.btn_local_files.setText(_translate("Form", "Local files"))

