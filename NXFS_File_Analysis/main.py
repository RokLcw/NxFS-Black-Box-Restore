from PyQt5 import QtCore, QtGui, QtWidgets,uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QApplication, QPushButton,QHBoxLayout,QWidget
import sys
from time import sleep
import os, time
from collections import deque
import binascii

class Ui_MainWindow(object):
    
    def __init__(self):
        super().__init__()
    
    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1110, 800)
        MainWindow.setWindowIcon(QtGui.QIcon('C:/Users/revib/OneDrive_hallym/바탕 화면/BOB/트랙교육/윤상혁멘토/프로젝트/UI/Re/LOGO.png'))
        
        self.tabWidget = QtWidgets.QTabWidget(MainWindow)
        self.tabWidget.setGeometry(QtCore.QRect(20, 10, 1050, 750))
        self.tabWidget.setStyleSheet("style\n" "rgb(255, 255, 127)")
        self.tabWidget.setObjectName("tabWidget")
        
        #tab안에 들어갈 object들 정의
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("Home_tab")
        
        #FileButton Ui
        self.FileButton = QtWidgets.QPushButton(self.tab)
        self.FileButton.setGeometry(QtCore.QRect(30, 40, 81, 31))
        self.FileButton.setObjectName("FileButton")
        
        #FileInfo Ui
        self.FileInfoWidget = QtWidgets.QTreeWidget(self.tab) # home의 widget
        self.FileInfoWidget.setGeometry(QtCore.QRect(30, 80, 985, 600))
        self.FileInfoWidget.setObjectName("FileInfoWidget")
        
        #qtreewidget의 옵션들이 굉장히 많다. 여기서 잘 조합하면 treewidget 변경 가능.
        self.FileInfoWidget.setColumnCount(2)
        self.FileInfoWidget.setHeaderLabels(['property','value']) # property header


        self.ParsingButton = QtWidgets.QPushButton(self.tab)
        self.ParsingButton.setGeometry(QtCore.QRect(920, 39, 93, 31))
        self.ParsingButton.setObjectName("ParsingButton")
        
        self.tabWidget.addTab(self.tab, "")

        
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        
        
        '''
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.tabWidget.addTab(self.tab_3, "")
        
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.tabWidget.addTab(self.tab_4, "")
        '''
        self.retranslateUi(MainWindow)
        #self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    
    
    def retranslateUi(self, MainWindow):        # ui -> 기능 연결점
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "NXFS"))
        
        
        self.FileButton.setText(_translate("Form", "File"))
        self.ParsingButton.setText(_translate("MainWindow", "Parsing"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Home"))
       
        
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Assigned"))
        
        #self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Non-assigned"))
        #self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "Slack"))

        self.FileButton.clicked.connect(self.openfile_handler)
        self.ParsingButton.clicked.connect(self.parsing_handler)

        
    def openfile_handler(self):     # file open dialog
        global path
        file=QFileDialog.getOpenFileName(widget,"Open Single File","","All Files(*)")
        path = file[0]
        self.fileInfo()
        
        
    def fileInfo(self):         # file information home page에 띄워주는 기능
        global path

        _translate = QtCore.QCoreApplication.translate
        
        
        meta = {'File': path,
        'Extension': path.lstrip('.') , 
        'Access time': time.ctime(os.path.getatime(path)),
        'Modified time': time.ctime(os.path.getmtime(path)),
        'Change time': time.ctime(os.path.getctime(path)),
        'Size' : '%.2f KB' % (os.path.getsize(path)/ (1024.0))}
        
        key=[]
        val=[]
        for i,j in meta.items():
            key.append(i)
            val.append(j)
            item_0 = QtWidgets.QTreeWidgetItem(self.FileInfoWidget)
            
            num = 0
        while num<6:
            if num ==0:
                self.FileInfoWidget.topLevelItem(num).setText(0, _translate("MainWindow", key[num])) 
                self.FileInfoWidget.topLevelItem(num).setText(1, _translate("MainWindow", val[num]))
            if num ==1:
                self.FileInfoWidget.topLevelItem(num).setText(0, _translate("MainWindow", key[num])) 
                self.FileInfoWidget.topLevelItem(num).setText(1, _translate("MainWindow", val[num]))
            if num ==2:
                self.FileInfoWidget.topLevelItem(num).setText(0, _translate("MainWindow", key[num])) 
                self.FileInfoWidget.topLevelItem(num).setText(1, _translate("MainWindow", val[num]))
            if num ==3:
                self.FileInfoWidget.topLevelItem(num).setText(0, _translate("MainWindow", key[num])) 
                self.FileInfoWidget.topLevelItem(num).setText(1, _translate("MainWindow", val[num]))
            if num ==4:
                self.FileInfoWidget.topLevelItem(num).setText(0, _translate("MainWindow", key[num])) 
                self.FileInfoWidget.topLevelItem(num).setText(1, _translate("MainWindow", val[num]))
            if num ==5:
                self.FileInfoWidget.topLevelItem(num).setText(0, _translate("MainWindow", key[num])) 
                self.FileInfoWidget.topLevelItem(num).setText(1, _translate("MainWindow", val[num]))
                
        
            num +=1
        
    
    def parsing_handler(self):
        self.tabWidget.setCurrentIndex(1)  # 화면 전환 Home -> Assigned page
        
        
        
        

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    widget = QtWidgets.QWidget()
    ui = Ui_MainWindow()      #class로 정의한 UI Window
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())