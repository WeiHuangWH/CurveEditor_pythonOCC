# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sketchProperty.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SketchProperty(object):
    def setupUi(self, SketchProperty):
        SketchProperty.setObjectName("SketchProperty")
        SketchProperty.resize(270, 325)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(SketchProperty)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.TextLabelID = QtWidgets.QLabel(SketchProperty)
        self.TextLabelID.setObjectName("TextLabelID")
        self.horizontalLayout_6.addWidget(self.TextLabelID)
        self.LineEditID = QtWidgets.QLineEdit(SketchProperty)
        self.LineEditID.setReadOnly(True)
        self.LineEditID.setObjectName("LineEditID")
        self.horizontalLayout_6.addWidget(self.LineEditID)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.GroupBoxGP = QtWidgets.QGroupBox(SketchProperty)
        self.GroupBoxGP.setObjectName("GroupBoxGP")
        self.GroupBoxGPLayout = QtWidgets.QGridLayout(self.GroupBoxGP)
        self.GroupBoxGPLayout.setObjectName("GroupBoxGPLayout")
        self.TextLabelPoint1 = QtWidgets.QLabel(self.GroupBoxGP)
        self.TextLabelPoint1.setObjectName("TextLabelPoint1")
        self.GroupBoxGPLayout.addWidget(self.TextLabelPoint1, 0, 0, 1, 1)
        self.LineEditPoint1 = QtWidgets.QLineEdit(self.GroupBoxGP)
        self.LineEditPoint1.setObjectName("LineEditPoint1")
        self.GroupBoxGPLayout.addWidget(self.LineEditPoint1, 0, 1, 1, 1)
        self.verticalLayout_3.addWidget(self.GroupBoxGP)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.GroupBoxAttributes = QtWidgets.QGroupBox(SketchProperty)
        self.GroupBoxAttributes.setObjectName("GroupBoxAttributes")
        self.GroupBoxAttributesLayout = QtWidgets.QGridLayout(self.GroupBoxAttributes)
        self.GroupBoxAttributesLayout.setObjectName("GroupBoxAttributesLayout")
        self.TextLabelColor = QtWidgets.QLabel(self.GroupBoxAttributes)
        self.TextLabelColor.setObjectName("TextLabelColor")
        self.GroupBoxAttributesLayout.addWidget(self.TextLabelColor, 0, 0, 1, 1)
        self.ComboBoxColor = QtWidgets.QComboBox(self.GroupBoxAttributes)
        self.ComboBoxColor.setObjectName("ComboBoxColor")
        self.ComboBoxColor.addItem("")
        self.ComboBoxColor.addItem("")
        self.ComboBoxColor.addItem("")
        self.ComboBoxColor.addItem("")
        self.ComboBoxColor.addItem("")
        self.GroupBoxAttributesLayout.addWidget(self.ComboBoxColor, 0, 1, 1, 1)
        self.TextLabelType = QtWidgets.QLabel(self.GroupBoxAttributes)
        self.TextLabelType.setObjectName("TextLabelType")
        self.GroupBoxAttributesLayout.addWidget(self.TextLabelType, 1, 0, 1, 1)
        self.ComboBoxType = QtWidgets.QComboBox(self.GroupBoxAttributes)
        self.ComboBoxType.setObjectName("ComboBoxType")
        self.ComboBoxType.addItem("")
        self.ComboBoxType.addItem("")
        self.GroupBoxAttributesLayout.addWidget(self.ComboBoxType, 1, 1, 1, 1)
        self.TextLabelStyle = QtWidgets.QLabel(self.GroupBoxAttributes)
        self.TextLabelStyle.setObjectName("TextLabelStyle")
        self.GroupBoxAttributesLayout.addWidget(self.TextLabelStyle, 2, 0, 1, 1)
        self.ComboBoxStyle = QtWidgets.QComboBox(self.GroupBoxAttributes)
        self.ComboBoxStyle.setObjectName("ComboBoxStyle")
        self.ComboBoxStyle.addItem("")
        self.ComboBoxStyle.addItem("")
        self.ComboBoxStyle.addItem("")
        self.ComboBoxStyle.addItem("")
        self.GroupBoxAttributesLayout.addWidget(self.ComboBoxStyle, 2, 1, 1, 1)
        self.TextLabelWidth = QtWidgets.QLabel(self.GroupBoxAttributes)
        self.TextLabelWidth.setObjectName("TextLabelWidth")
        self.GroupBoxAttributesLayout.addWidget(self.TextLabelWidth, 3, 0, 1, 1)
        self.ComboBoxWidth = QtWidgets.QComboBox(self.GroupBoxAttributes)
        self.ComboBoxWidth.setObjectName("ComboBoxWidth")
        self.ComboBoxWidth.addItem("")
        self.ComboBoxWidth.addItem("")
        self.ComboBoxWidth.addItem("")
        self.ComboBoxWidth.addItem("")
        self.ComboBoxWidth.addItem("")
        self.ComboBoxWidth.addItem("")
        self.ComboBoxWidth.addItem("")
        self.ComboBoxWidth.addItem("")
        self.ComboBoxWidth.addItem("")
        self.GroupBoxAttributesLayout.addWidget(self.ComboBoxWidth, 3, 1, 1, 1)
        self.verticalLayout_3.addWidget(self.GroupBoxAttributes)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.PushButtonOK = QtWidgets.QPushButton(SketchProperty)
        self.PushButtonOK.setObjectName("PushButtonOK")
        self.horizontalLayout_7.addWidget(self.PushButtonOK)
        self.PushButtonCancel = QtWidgets.QPushButton(SketchProperty)
        self.PushButtonCancel.setObjectName("PushButtonCancel")
        self.horizontalLayout_7.addWidget(self.PushButtonCancel)
        self.PushButtonApply = QtWidgets.QPushButton(SketchProperty)
        self.PushButtonApply.setObjectName("PushButtonApply")
        self.horizontalLayout_7.addWidget(self.PushButtonApply)
        self.verticalLayout_3.addLayout(self.horizontalLayout_7)

        self.retranslateUi(SketchProperty)
        QtCore.QMetaObject.connectSlotsByName(SketchProperty)

    def retranslateUi(self, SketchProperty):
        _translate = QtCore.QCoreApplication.translate
        SketchProperty.setWindowTitle(_translate("SketchProperty", "Form"))
        self.TextLabelID.setText(_translate("SketchProperty", "ID"))
        self.GroupBoxGP.setTitle(_translate("SketchProperty", "Geometry Properties"))
        self.TextLabelPoint1.setText(_translate("SketchProperty", "Point"))
        self.GroupBoxAttributes.setTitle(_translate("SketchProperty", "Attributes"))
        self.TextLabelColor.setText(_translate("SketchProperty", "Color"))
        self.ComboBoxColor.setItemText(0, _translate("SketchProperty", "BLACK"))
        self.ComboBoxColor.setItemText(1, _translate("SketchProperty", "BROWN"))
        self.ComboBoxColor.setItemText(2, _translate("SketchProperty", "RED"))
        self.ComboBoxColor.setItemText(3, _translate("SketchProperty", "ORANGE"))
        self.ComboBoxColor.setItemText(4, _translate("SketchProperty", "YELLOW"))
        self.TextLabelType.setText(_translate("SketchProperty", "Type"))
        self.ComboBoxType.setItemText(0, _translate("SketchProperty", "Main"))
        self.ComboBoxType.setItemText(1, _translate("SketchProperty", "Auxiliary"))
        self.TextLabelStyle.setText(_translate("SketchProperty", "Style"))
        self.ComboBoxStyle.setItemText(0, _translate("SketchProperty", "SOLID"))
        self.ComboBoxStyle.setItemText(1, _translate("SketchProperty", "DASH"))
        self.ComboBoxStyle.setItemText(2, _translate("SketchProperty", "DOT"))
        self.ComboBoxStyle.setItemText(3, _translate("SketchProperty", "DOTDASH"))
        self.TextLabelWidth.setText(_translate("SketchProperty", "Width"))
        self.ComboBoxWidth.setItemText(0, _translate("SketchProperty", "1.0"))
        self.ComboBoxWidth.setItemText(1, _translate("SketchProperty", "2.0"))
        self.ComboBoxWidth.setItemText(2, _translate("SketchProperty", "3.0"))
        self.ComboBoxWidth.setItemText(3, _translate("SketchProperty", "4.0"))
        self.ComboBoxWidth.setItemText(4, _translate("SketchProperty", "5.0"))
        self.ComboBoxWidth.setItemText(5, _translate("SketchProperty", "6.0"))
        self.ComboBoxWidth.setItemText(6, _translate("SketchProperty", "7.0"))
        self.ComboBoxWidth.setItemText(7, _translate("SketchProperty", "8.0"))
        self.ComboBoxWidth.setItemText(8, _translate("SketchProperty", "9.0"))
        self.PushButtonOK.setText(_translate("SketchProperty", "Ok"))
        self.PushButtonCancel.setText(_translate("SketchProperty", "Cancel"))
        self.PushButtonApply.setText(_translate("SketchProperty", "Apply"))