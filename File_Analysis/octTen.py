# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '20221005.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

'''
Now : making file dialog with print filename which is clicked
'''

from PyQt5 import QtCore, QtGui, QtWidgets,uic
from fileopen import Ui_FileOpen
#fileopen.py에서 Ui_FileOpen class를 가져오기
from PyQt5.QtWidgets import *
import sys
from time import sleep
import os, time



class Ui_MainWindow(object):       
       
    def openFileDialog(self):           #File open 창 
        option=QFileDialog.Options()
        file=QFileDialog.getOpenFileName(widget,"Open Single File","","All Files(*)",options=option)
        path = file[0]                  
        
        split_t = os.path.splitext(path)
        file_extension = split_t[1]
        

        print('File         :', path)
        print('Extension    :', file_extension.lstrip('.'))
        print('Access time  :', time.ctime(os.path.getatime(path)))
        print('Modified time:', time.ctime(os.path.getmtime(path)))
        print('Change time  :', time.ctime(os.path.getctime(path)))
        print('Size         :', os.path.getsize(path))
        
        
        
        sleep(1)
        sys.exit()
        
        
    def fileInfo(self):
        
    
    
        
        
        #### Ui -> py 변환
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1115, 801)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(60, 20, 971, 701))
        self.tabWidget.setStyleSheet("style\n"
"rgb(255, 255, 127)")
        self.tabWidget.setObjectName("tabWidget")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.FileButton = QtWidgets.QPushButton(self.tab_4, clicked=lambda:self.openFileDialog() )
        #self.FileButton.clicked.connect(self.openFileDialog)
        # 기능을 넣고자 하는 곳에 새롭게 만든 기능 연결
        self.FileButton.setGeometry(QtCore.QRect(10, 10, 81, 31))
        self.FileButton.setAcceptDrops(False)
        self.FileButton.setObjectName("FileButton")
        self.HomeGroupbox = QtWidgets.QGroupBox(self.tab_4)
        self.HomeGroupbox.setGeometry(QtCore.QRect(10, 80, 941, 581))
        self.HomeGroupbox.setTitle("")
        self.HomeGroupbox.setObjectName("HomeGroupbox")
        
        
        self.FileInfoWidget = QtWidgets.QTreeWidget(self.HomeGroupbox) # home의 widget
        self.FileInfoWidget.setGeometry(QtCore.QRect(70, 50, 861, 491))
        self.FileInfoWidget.setTabletTracking(False)
        self.FileInfoWidget.setAutoFillBackground(False)
        self.FileInfoWidget.setUniformRowHeights(False)
        self.FileInfoWidget.setItemsExpandable(False)
        self.FileInfoWidget.setObjectName("FileInfoWidget")
        self.FileInfoWidget.headerItem().setTextAlignment(0, QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.FileInfoWidget.headerItem().setFont(0, font)
        self.FileInfoWidget.headerItem().setTextAlignment(1, QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.FileInfoWidget.headerItem().setFont(1, font)
        self.FileInfoWidget.headerItem().setTextAlignment(2, QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(11)
        self.FileInfoWidget.headerItem().setFont(2, font)
        self.FileInfoWidget.headerItem().setTextAlignment(3, QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(11)
        self.FileInfoWidget.headerItem().setFont(3, font)
        self.FileInfoWidget.headerItem().setTextAlignment(4, QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(11)
        self.FileInfoWidget.headerItem().setFont(4, font)
        self.FileInfoWidget.headerItem().setTextAlignment(5, QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(11)
        self.FileInfoWidget.headerItem().setFont(5, font)
        item_0 = QtWidgets.QTreeWidgetItem(self.FileInfoWidget)
        item_0 = QtWidgets.QTreeWidgetItem(self.FileInfoWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        item_0.setFont(0, font)
        
        
        self.ParsingButton = QtWidgets.QPushButton(self.tab_4)
        self.ParsingButton.setGeometry(QtCore.QRect(850, 40, 93, 31))
        self.ParsingButton.setObjectName("ParsingButton")
        self.tabWidget.addTab(self.tab_4, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.groupBox = QtWidgets.QGroupBox(self.tab)
        self.groupBox.setGeometry(QtCore.QRect(300, 50, 661, 571))
        self.groupBox.setObjectName("groupBox")
        self.checkBox = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox.setGeometry(QtCore.QRect(0, 120, 601, 19))
        self.checkBox.setObjectName("checkBox")
        self.checkBox_2 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_2.setGeometry(QtCore.QRect(0, 220, 601, 19))
        self.checkBox_2.setObjectName("checkBox_2")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(0, 150, 91, 16))
        self.label.setStyleSheet("asd\n"
"rgb(238, 255, 197)")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(100, 150, 91, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(180, 150, 91, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(280, 150, 91, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(370, 150, 91, 16))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(460, 150, 91, 16))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setGeometry(QtCore.QRect(540, 150, 61, 16))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.groupBox)
        self.label_8.setGeometry(QtCore.QRect(280, 170, 91, 16))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.groupBox)
        self.label_9.setGeometry(QtCore.QRect(370, 170, 91, 16))
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.groupBox)
        self.label_10.setGeometry(QtCore.QRect(540, 170, 61, 16))
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.groupBox)
        self.label_11.setGeometry(QtCore.QRect(180, 170, 91, 16))
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.groupBox)
        self.label_12.setGeometry(QtCore.QRect(460, 170, 91, 16))
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.groupBox)
        self.label_13.setGeometry(QtCore.QRect(100, 170, 91, 16))
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(self.groupBox)
        self.label_14.setGeometry(QtCore.QRect(0, 170, 91, 16))
        self.label_14.setStyleSheet("asd\n"
"rgb(238, 255, 197)")
        self.label_14.setObjectName("label_14")
        self.label_15 = QtWidgets.QLabel(self.groupBox)
        self.label_15.setGeometry(QtCore.QRect(180, 190, 91, 16))
        self.label_15.setObjectName("label_15")
        self.label_16 = QtWidgets.QLabel(self.groupBox)
        self.label_16.setGeometry(QtCore.QRect(540, 190, 61, 16))
        self.label_16.setObjectName("label_16")
        self.label_17 = QtWidgets.QLabel(self.groupBox)
        self.label_17.setGeometry(QtCore.QRect(280, 190, 91, 16))
        self.label_17.setObjectName("label_17")
        self.label_18 = QtWidgets.QLabel(self.groupBox)
        self.label_18.setGeometry(QtCore.QRect(460, 190, 91, 16))
        self.label_18.setObjectName("label_18")
        self.label_19 = QtWidgets.QLabel(self.groupBox)
        self.label_19.setGeometry(QtCore.QRect(0, 190, 91, 16))
        self.label_19.setStyleSheet("asd\n"
"rgb(238, 255, 197)")
        self.label_19.setObjectName("label_19")
        self.label_20 = QtWidgets.QLabel(self.groupBox)
        self.label_20.setGeometry(QtCore.QRect(370, 190, 91, 16))
        self.label_20.setObjectName("label_20")
        self.label_21 = QtWidgets.QLabel(self.groupBox)
        self.label_21.setGeometry(QtCore.QRect(100, 190, 91, 16))
        self.label_21.setObjectName("label_21")
        self.label_22 = QtWidgets.QLabel(self.groupBox)
        self.label_22.setGeometry(QtCore.QRect(180, 250, 91, 16))
        self.label_22.setObjectName("label_22")
        self.label_23 = QtWidgets.QLabel(self.groupBox)
        self.label_23.setGeometry(QtCore.QRect(460, 250, 91, 16))
        self.label_23.setObjectName("label_23")
        self.label_24 = QtWidgets.QLabel(self.groupBox)
        self.label_24.setGeometry(QtCore.QRect(280, 250, 91, 16))
        self.label_24.setObjectName("label_24")
        self.label_25 = QtWidgets.QLabel(self.groupBox)
        self.label_25.setGeometry(QtCore.QRect(540, 250, 61, 16))
        self.label_25.setObjectName("label_25")
        self.label_26 = QtWidgets.QLabel(self.groupBox)
        self.label_26.setGeometry(QtCore.QRect(370, 250, 91, 16))
        self.label_26.setObjectName("label_26")
        self.label_27 = QtWidgets.QLabel(self.groupBox)
        self.label_27.setGeometry(QtCore.QRect(0, 250, 91, 16))
        self.label_27.setStyleSheet("asd\n"
"rgb(238, 255, 197)")
        self.label_27.setObjectName("label_27")
        self.label_28 = QtWidgets.QLabel(self.groupBox)
        self.label_28.setGeometry(QtCore.QRect(100, 250, 91, 16))
        self.label_28.setObjectName("label_28")
        self.label_29 = QtWidgets.QLabel(self.groupBox)
        self.label_29.setGeometry(QtCore.QRect(460, 270, 91, 16))
        self.label_29.setObjectName("label_29")
        self.label_30 = QtWidgets.QLabel(self.groupBox)
        self.label_30.setGeometry(QtCore.QRect(540, 270, 61, 16))
        self.label_30.setObjectName("label_30")
        self.label_31 = QtWidgets.QLabel(self.groupBox)
        self.label_31.setGeometry(QtCore.QRect(100, 270, 91, 16))
        self.label_31.setObjectName("label_31")
        self.label_32 = QtWidgets.QLabel(self.groupBox)
        self.label_32.setGeometry(QtCore.QRect(0, 270, 91, 16))
        self.label_32.setStyleSheet("asd\n"
"rgb(238, 255, 197)")
        self.label_32.setObjectName("label_32")
        self.label_33 = QtWidgets.QLabel(self.groupBox)
        self.label_33.setGeometry(QtCore.QRect(280, 270, 91, 16))
        self.label_33.setObjectName("label_33")
        self.label_34 = QtWidgets.QLabel(self.groupBox)
        self.label_34.setGeometry(QtCore.QRect(370, 270, 91, 16))
        self.label_34.setObjectName("label_34")
        self.label_35 = QtWidgets.QLabel(self.groupBox)
        self.label_35.setGeometry(QtCore.QRect(180, 270, 91, 16))
        self.label_35.setObjectName("label_35")
        self.label_36 = QtWidgets.QLabel(self.groupBox)
        self.label_36.setGeometry(QtCore.QRect(460, 290, 91, 16))
        self.label_36.setObjectName("label_36")
        self.label_37 = QtWidgets.QLabel(self.groupBox)
        self.label_37.setGeometry(QtCore.QRect(280, 290, 91, 16))
        self.label_37.setObjectName("label_37")
        self.label_38 = QtWidgets.QLabel(self.groupBox)
        self.label_38.setGeometry(QtCore.QRect(180, 290, 91, 16))
        self.label_38.setObjectName("label_38")
        self.label_39 = QtWidgets.QLabel(self.groupBox)
        self.label_39.setGeometry(QtCore.QRect(370, 290, 91, 16))
        self.label_39.setObjectName("label_39")
        self.label_40 = QtWidgets.QLabel(self.groupBox)
        self.label_40.setGeometry(QtCore.QRect(100, 290, 91, 16))
        self.label_40.setObjectName("label_40")
        self.label_41 = QtWidgets.QLabel(self.groupBox)
        self.label_41.setGeometry(QtCore.QRect(0, 290, 91, 16))
        self.label_41.setStyleSheet("asd\n"
"rgb(238, 255, 197)")
        self.label_41.setObjectName("label_41")
        self.label_42 = QtWidgets.QLabel(self.groupBox)
        self.label_42.setGeometry(QtCore.QRect(540, 290, 61, 16))
        self.label_42.setObjectName("label_42")
        self.label_43 = QtWidgets.QLabel(self.groupBox)
        self.label_43.setGeometry(QtCore.QRect(460, 460, 91, 16))
        self.label_43.setObjectName("label_43")
        self.label_44 = QtWidgets.QLabel(self.groupBox)
        self.label_44.setGeometry(QtCore.QRect(100, 460, 91, 16))
        self.label_44.setObjectName("label_44")
        self.label_45 = QtWidgets.QLabel(self.groupBox)
        self.label_45.setGeometry(QtCore.QRect(370, 460, 91, 16))
        self.label_45.setObjectName("label_45")
        self.label_46 = QtWidgets.QLabel(self.groupBox)
        self.label_46.setGeometry(QtCore.QRect(370, 440, 91, 16))
        self.label_46.setObjectName("label_46")
        self.label_47 = QtWidgets.QLabel(self.groupBox)
        self.label_47.setGeometry(QtCore.QRect(0, 440, 91, 16))
        self.label_47.setStyleSheet("asd\n"
"rgb(238, 255, 197)")
        self.label_47.setObjectName("label_47")
        self.label_48 = QtWidgets.QLabel(self.groupBox)
        self.label_48.setGeometry(QtCore.QRect(540, 460, 61, 16))
        self.label_48.setObjectName("label_48")
        self.label_49 = QtWidgets.QLabel(self.groupBox)
        self.label_49.setGeometry(QtCore.QRect(100, 420, 91, 16))
        self.label_49.setObjectName("label_49")
        self.label_50 = QtWidgets.QLabel(self.groupBox)
        self.label_50.setGeometry(QtCore.QRect(370, 420, 91, 16))
        self.label_50.setObjectName("label_50")
        self.label_51 = QtWidgets.QLabel(self.groupBox)
        self.label_51.setGeometry(QtCore.QRect(180, 420, 91, 16))
        self.label_51.setObjectName("label_51")
        self.label_52 = QtWidgets.QLabel(self.groupBox)
        self.label_52.setGeometry(QtCore.QRect(280, 440, 91, 16))
        self.label_52.setObjectName("label_52")
        self.label_53 = QtWidgets.QLabel(self.groupBox)
        self.label_53.setGeometry(QtCore.QRect(460, 440, 91, 16))
        self.label_53.setObjectName("label_53")
        self.label_54 = QtWidgets.QLabel(self.groupBox)
        self.label_54.setGeometry(QtCore.QRect(460, 420, 91, 16))
        self.label_54.setObjectName("label_54")
        self.label_55 = QtWidgets.QLabel(self.groupBox)
        self.label_55.setGeometry(QtCore.QRect(180, 440, 91, 16))
        self.label_55.setObjectName("label_55")
        self.label_56 = QtWidgets.QLabel(self.groupBox)
        self.label_56.setGeometry(QtCore.QRect(180, 460, 91, 16))
        self.label_56.setObjectName("label_56")
        self.label_57 = QtWidgets.QLabel(self.groupBox)
        self.label_57.setGeometry(QtCore.QRect(280, 460, 91, 16))
        self.label_57.setObjectName("label_57")
        self.label_58 = QtWidgets.QLabel(self.groupBox)
        self.label_58.setGeometry(QtCore.QRect(100, 440, 91, 16))
        self.label_58.setObjectName("label_58")
        self.label_59 = QtWidgets.QLabel(self.groupBox)
        self.label_59.setGeometry(QtCore.QRect(280, 420, 91, 16))
        self.label_59.setObjectName("label_59")
        self.label_60 = QtWidgets.QLabel(self.groupBox)
        self.label_60.setGeometry(QtCore.QRect(540, 420, 61, 16))
        self.label_60.setObjectName("label_60")
        self.label_61 = QtWidgets.QLabel(self.groupBox)
        self.label_61.setGeometry(QtCore.QRect(0, 420, 91, 16))
        self.label_61.setStyleSheet("asd\n"
"rgb(238, 255, 197)")
        self.label_61.setObjectName("label_61")
        self.label_62 = QtWidgets.QLabel(self.groupBox)
        self.label_62.setGeometry(QtCore.QRect(0, 460, 91, 16))
        self.label_62.setStyleSheet("asd\n"
"rgb(238, 255, 197)")
        self.label_62.setObjectName("label_62")
        self.label_63 = QtWidgets.QLabel(self.groupBox)
        self.label_63.setGeometry(QtCore.QRect(540, 440, 61, 16))
        self.label_63.setObjectName("label_63")
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit.setGeometry(QtCore.QRect(0, 390, 601, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_2.setGeometry(QtCore.QRect(0, 80, 601, 21))
        self.lineEdit_2.setStyleSheet("style\n"
"rgb(170, 255, 255)")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.treeWidget_2 = QtWidgets.QTreeWidget(self.tab)
        self.treeWidget_2.setGeometry(QtCore.QRect(0, 50, 271, 571))
        self.treeWidget_2.setObjectName("treeWidget_2")
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget_2)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget_2)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget_2)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget_2)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget_2)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget_2)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        self.progressBar = QtWidgets.QProgressBar(self.tab)
        self.progressBar.setGeometry(QtCore.QRect(0, 650, 941, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.verticalScrollBar = QtWidgets.QScrollBar(self.tab)
        self.verticalScrollBar.setGeometry(QtCore.QRect(260, 50, 20, 571))
        self.verticalScrollBar.setOrientation(QtCore.Qt.Vertical)
        self.verticalScrollBar.setObjectName("verticalScrollBar")
        self.treeWidget_2.raise_()
        self.progressBar.raise_()
        self.verticalScrollBar.raise_()
        self.groupBox.raise_()
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.tabWidget.addTab(self.tab_3, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1115, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.FileButton.setText(_translate("MainWindow", "File"))
        self.FileInfoWidget.setToolTip(_translate("MainWindow", "<html><head/><body><p>asdad</p></body></html>"))
        self.FileInfoWidget.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>qda</p></body></html>"))
        self.FileInfoWidget.headerItem().setText(0, _translate("MainWindow", "File Name"))
        self.FileInfoWidget.headerItem().setText(1, _translate("MainWindow", "Extension"))
        self.FileInfoWidget.headerItem().setText(2, _translate("MainWindow", "File size"))
        self.FileInfoWidget.headerItem().setText(3, _translate("MainWindow", "created time"))
        self.FileInfoWidget.headerItem().setText(4, _translate("MainWindow", "modified time"))
        self.FileInfoWidget.headerItem().setText(5, _translate("MainWindow", "accessed time"))
        __sortingEnabled = self.FileInfoWidget.isSortingEnabled()
        self.FileInfoWidget.setSortingEnabled(False)
        self.FileInfoWidget.topLevelItem(1).setText(0, _translate("MainWindow", "새 항목"))
        self.FileInfoWidget.topLevelItem(1).setText(1, _translate("MainWindow", ".avi"))
        self.FileInfoWidget.topLevelItem(1).setText(2, _translate("MainWindow", "1234kb"))
        self.FileInfoWidget.topLevelItem(1).setText(3, _translate("MainWindow", "yy-mm-dd 12:00:00"))
        self.FileInfoWidget.setSortingEnabled(__sortingEnabled)
        self.ParsingButton.setText(_translate("MainWindow", "Parsing"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "Home"))
        self.groupBox.setTitle(_translate("MainWindow", "Analyzed"))
        self.checkBox.setText(_translate("MainWindow", "    Available 1"))
        self.checkBox_2.setText(_translate("MainWindow", "    Available 2"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#5555ff;\">000001.dat</span></p></body></html>"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#5555ff;\">126446 KB</span></p></body></html>"))
        self.label_3.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#5555ff;\">0000015a5b3</span></p></body></html>"))
        self.label_4.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#5555ff;\">12:00</span></p></body></html>"))
        self.label_5.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#5555ff;\">12:01</span></p></body></html>"))
        self.label_6.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#5555ff;\">01</span></p></body></html>"))
        self.label_7.setText(_translate("MainWindow", "..."))
        self.label_8.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#5555ff;\">12:00</span></p></body></html>"))
        self.label_9.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#5555ff;\">12:01</span></p></body></html>"))
        self.label_10.setText(_translate("MainWindow", "..."))
        self.label_11.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#5555ff;\">0000015a5b3</span></p></body></html>"))
        self.label_12.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#5555ff;\">01</span></p></body></html>"))
        self.label_13.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#5555ff;\">126446 KB</span></p></body></html>"))
        self.label_14.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#5555ff;\">000002.dat</span></p></body></html>"))
        self.label_15.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#5555ff;\">0000015a5b3</span></p></body></html>"))
        self.label_16.setText(_translate("MainWindow", "..."))
        self.label_17.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#5555ff;\">12:00</span></p></body></html>"))
        self.label_18.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#5555ff;\">01</span></p></body></html>"))
        self.label_19.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#5555ff;\">000003.dat</span></p></body></html>"))
        self.label_20.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#5555ff;\">12:01</span></p></body></html>"))
        self.label_21.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#5555ff;\">126446 KB</span></p></body></html>"))
        self.label_22.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#5555ff;\">0000015a5b3</span></p></body></html>"))
        self.label_23.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#5555ff;\">01</span></p></body></html>"))
        self.label_24.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#5555ff;\">12:00</span></p></body></html>"))
        self.label_25.setText(_translate("MainWindow", "..."))
        self.label_26.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#5555ff;\">12:01</span></p></body></html>"))
        self.label_27.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#5555ff;\">000004.dat</span></p></body></html>"))
        self.label_28.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#5555ff;\">126446 KB</span></p></body></html>"))
        self.label_29.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#5555ff;\">01</span></p></body></html>"))
        self.label_30.setText(_translate("MainWindow", "..."))
        self.label_31.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#5555ff;\">126446 KB</span></p></body></html>"))
        self.label_32.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#5555ff;\">000005.dat</span></p></body></html>"))
        self.label_33.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#5555ff;\">12:00</span></p></body></html>"))
        self.label_34.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#5555ff;\">12:01</span></p></body></html>"))
        self.label_35.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#5555ff;\">0000015a5b3</span></p></body></html>"))
        self.label_36.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#5555ff;\">01</span></p></body></html>"))
        self.label_37.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#5555ff;\">12:00</span></p></body></html>"))
        self.label_38.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#5555ff;\">0000015a5b3</span></p></body></html>"))
        self.label_39.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#5555ff;\">12:01</span></p></body></html>"))
        self.label_40.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#5555ff;\">126446 KB</span></p></body></html>"))
        self.label_41.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#5555ff;\">000006.dat</span></p></body></html>"))
        self.label_42.setText(_translate("MainWindow", "..."))
        self.label_43.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#5555ff;\">01</span></p></body></html>"))
        self.label_44.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#5555ff;\">126446 KB</span></p></body></html>"))
        self.label_45.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#5555ff;\">12:01</span></p></body></html>"))
        self.label_46.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#5555ff;\">12:01</span></p></body></html>"))
        self.label_47.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" color:#5555ff;\">?</span></p></body></html>"))
        self.label_48.setText(_translate("MainWindow", "..."))
        self.label_49.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#5555ff;\">126446 KB</span></p></body></html>"))
        self.label_50.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#5555ff;\">12:01</span></p></body></html>"))
        self.label_51.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#5555ff;\">41b5c13a1</span></p></body></html>"))
        self.label_52.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#5555ff;\">12:00</span></p></body></html>"))
        self.label_53.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#5555ff;\">01</span></p></body></html>"))
        self.label_54.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#5555ff;\">01</span></p></body></html>"))
        self.label_55.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#5555ff;\">0000015a5b3</span></p></body></html>"))
        self.label_56.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#5555ff;\">0000015a5b3</span></p></body></html>"))
        self.label_57.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#5555ff;\">12:00</span></p></body></html>"))
        self.label_58.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#5555ff;\">126446 KB</span></p></body></html>"))
        self.label_59.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#5555ff;\">12:00</span></p></body></html>"))
        self.label_60.setText(_translate("MainWindow", "..."))
        self.label_61.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">?</p></body></html>"))
        self.label_62.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" color:#5555ff;\">?</span></p></body></html>"))
        self.label_63.setText(_translate("MainWindow", "..."))
        self.lineEdit.setText(_translate("MainWindow", "Slack"))
        self.lineEdit_2.setText(_translate("MainWindow", "Non-assigned"))
        self.treeWidget_2.headerItem().setText(0, _translate("MainWindow", "0000001.nxfs"))
        __sortingEnabled = self.treeWidget_2.isSortingEnabled()
        self.treeWidget_2.setSortingEnabled(False)
        self.treeWidget_2.topLevelItem(0).setText(0, _translate("MainWindow", "Assigned"))
        self.treeWidget_2.topLevelItem(1).setText(0, _translate("MainWindow", "Info"))
        self.treeWidget_2.topLevelItem(1).child(0).setText(0, _translate("MainWindow", "00001.avi"))
        self.treeWidget_2.topLevelItem(1).child(1).setText(0, _translate("MainWindow", "00002.avi"))
        self.treeWidget_2.topLevelItem(1).child(2).setText(0, _translate("MainWindow", "00003.avi"))
        self.treeWidget_2.topLevelItem(2).setText(0, _translate("MainWindow", "Event"))
        self.treeWidget_2.topLevelItem(2).child(0).setText(0, _translate("MainWindow", "00004.avi"))
        self.treeWidget_2.topLevelItem(2).child(1).setText(0, _translate("MainWindow", "00005.avi"))
        self.treeWidget_2.topLevelItem(3).setText(0, _translate("MainWindow", "Park"))
        self.treeWidget_2.topLevelItem(3).child(0).setText(0, _translate("MainWindow", "00006.avi"))
        self.treeWidget_2.topLevelItem(3).child(1).setText(0, _translate("MainWindow", "00007.avi"))
        self.treeWidget_2.topLevelItem(4).setText(0, _translate("MainWindow", "Non-assigned"))
        self.treeWidget_2.topLevelItem(4).child(0).setText(0, _translate("MainWindow", "available 1"))
        self.treeWidget_2.topLevelItem(4).child(0).child(0).setText(0, _translate("MainWindow", "SPS"))
        self.treeWidget_2.topLevelItem(4).child(0).child(1).setText(0, _translate("MainWindow", "PPS"))
        self.treeWidget_2.topLevelItem(4).child(0).child(2).setText(0, _translate("MainWindow", "iframe"))
        self.treeWidget_2.topLevelItem(4).child(0).child(3).setText(0, _translate("MainWindow", "pframe"))
        self.treeWidget_2.topLevelItem(4).child(1).setText(0, _translate("MainWindow", "available2"))
        self.treeWidget_2.topLevelItem(4).child(1).child(0).setText(0, _translate("MainWindow", "iframe"))
        self.treeWidget_2.topLevelItem(4).child(1).child(1).setText(0, _translate("MainWindow", "pframe"))
        self.treeWidget_2.topLevelItem(5).setText(0, _translate("MainWindow", "Slack"))
        self.treeWidget_2.topLevelItem(5).child(0).setText(0, _translate("MainWindow", "Non-identified"))
        self.treeWidget_2.topLevelItem(5).child(1).setText(0, _translate("MainWindow", "Non-identified(2)"))
        self.treeWidget_2.setSortingEnabled(__sortingEnabled)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Assigned"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Non-assigned"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Slack"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    widget = QWidget()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    
    

    MainWindow.show()
    sys.exit(app.exec_())
