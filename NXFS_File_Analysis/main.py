
from PyQt5 import QtCore, QtGui, QtWidgets,uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QApplication, QPushButton,QHBoxLayout,QWidget
import sys
from time import sleep
import os, time
from collections import deque
import binascii
import itertools
from hexdump import hexdump
import re


class Ui_MainWindow(object):
    
    def __init__(self):
        super().__init__()
        
    
    def openfile_handler(self):     # file open dialog
        global path
        file=QFileDialog.getOpenFileName(widget,"Open Single File","","All Files(*)")
        path = file[0]
        self.fileInfo()
        
        
    def fileInfo(self):         # file information home page에 띄워주는 기능
        global path
        global h1

        _translate = QtCore.QCoreApplication.translate
        
        
        meta = {'File': path,
        'Extension': path.lstrip('.') , 
        'Access time': time.ctime(os.path.getatime(path)),
        'Modified time': time.ctime(os.path.getmtime(path)),
        'Change time': time.ctime(os.path.getctime(path)),
        'Size' : '%.2f MB' % (os.path.getsize(path)/ (1024*1024))}
        
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
        
        self.tabWidget.setCurrentIndex(1)  # 화면 전환 Home -> Assigned page
        self.ParsingF() 
    
    
    def list_chuck(self,arr, n):                                    # [offset] [hex] [ascii] += [one array] 함수
        return [arr[i: i + n] for i in range(0, len(arr), n)]

        
    
    def ParsingF(self):                                             # hex parsing 함수
        global path
        global h1

        _translate = QtCore.QCoreApplication.translate
        self.groupBox.setTitle(_translate("MainWindow", "Analyzed"))
        
        
        
        if path:                             # offset, hex data, ascii data
            with open(path, 'rb') as fileObj:
                filedata = fileObj.read()   #readline 했더니, content의 line대로 읽음. read만 가능.

            #print(hexdump(filedata))    
        h = str(hexdump(filedata))          #hexdump -> str -> 한개씩 split.

        h1 = re.split(r'\n',h)       #헥스값 \n 줄단위 분리. h1[x]가 한줄
        #print(h1)
        #h2 = re.split(r'" "',h1)
        listexceptlast = h1[:-2]         ##마지막 줄만 제외. (range 오류남)
        lastline = h1[-2]

        L = lastline.split()             # 마지막줄
        
        
        offset = []
        h=[]
        a = []
        ascii=[]
        for i in listexceptlast:
            h2 = i.split(" ")              #" " 단위 split
            offset.append(h2[0])
            h.append(h2[1:18])
            a.append(h2[18:])

        for i in a:
            b = ' '.join(i)
            b = b.replace('|','')
            ascii.append(b)                #ascii list
            #print(b)



        
        aline = []
        x=0
        while x<len(offset):
            aline.append([offset[x]])
            aline.append(h[x])
            aline.append([ascii[x]])
            x+=1
        
        
    
        if len(L) > 9:
            L.insert(9, '')

    

        for s in L:                          #마지막 줄 포맷 정제
            if "|" in s:
                a = L.index(s)
                if a != len(L)-1:
                    s = L[a]+' '+L[a+1]
                    s = s.replace('|', '')
                    L[a] = s
                    del L[a+1]
                
                else:
                    s = s.replace('|', '')
                    L[a] = s
                    
        for i in range(19):
            if len(L[1:-1]) != 17:
                L.insert(-1,'')
        
        aline.append([L[0]])                #마지막줄까지 append
        aline.append(L[1:-1])
        aline.append([L[-1]])

        r = self.list_chuck(aline,3)
        
        
        hex=[]

        for i in r:
            li = list(itertools.chain(*i))
            hex += li
            #print(li)                       #완벽한 줄단위 완성
            
       

        #tablewidget setupUI code

        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.setRowCount(len(offset)+1)          #hex 줄 갯수 == row              
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(19)            #offset~Ascii 고정
    
        x=0
        
        for i in range(len(offset)+1):                  #tablewidget item setting
            for j in range(19): 
                if x<len(hex):
                    #for y in range(:-1)
                    tableitem = QtWidgets.QTableWidgetItem()
                    self.tableWidget.setItem(i,j,tableitem)
                    tableitem.setText(_translate("MainWindow", hex[x] ))   #data input
                    x+=1
                #print(x)
                #print(i)
                
        for i in range(19):                         # hex sequence header (0~F)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(i, item)
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "OFFSET"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "0"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "1"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "2"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "3"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "4"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "5"))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "6"))
        item = self.tableWidget.horizontalHeaderItem(8)
        item.setText(_translate("MainWindow", "7"))
        item = self.tableWidget.horizontalHeaderItem(9)
        item.setText(_translate("MainWindow", ""))
        item = self.tableWidget.horizontalHeaderItem(10)
        item.setText(_translate("MainWindow", "8"))
        item = self.tableWidget.horizontalHeaderItem(11)
        item.setText(_translate("MainWindow", "9"))
        item = self.tableWidget.horizontalHeaderItem(12)
        item.setText(_translate("MainWindow", "A"))
        item = self.tableWidget.horizontalHeaderItem(13)
        item.setText(_translate("MainWindow", "B"))
        item = self.tableWidget.horizontalHeaderItem(14)
        item.setText(_translate("MainWindow", "C"))
        item = self.tableWidget.horizontalHeaderItem(15)
        item.setText(_translate("MainWindow", "D"))
        item = self.tableWidget.horizontalHeaderItem(16)
        item.setText(_translate("MainWindow", "E"))
        item = self.tableWidget.horizontalHeaderItem(17)
        item.setText(_translate("MainWindow", "F"))
        item = self.tableWidget.horizontalHeaderItem(18)
        item.setText(_translate("MainWindow", "ASCII"))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)                               #widget appearance setting
        self.tableWidget.setSortingEnabled(__sortingEnabled)
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()
        self.tableWidget.horizontalHeader().resizeSection(0,100)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        
        self.tableWidget.setSortingEnabled(__sortingEnabled)
        
    
        
    
    def setupUi(self, MainWindow):
        global h1
        
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1400, 900)
        MainWindow.setWindowIcon(QtGui.QIcon('C:/Users/revib/OneDrive_hallym/바탕 화면/BOB/트랙교육/윤상혁멘토/프로젝트/UI/Re/LOGO.png'))
        
        self.tabWidget = QtWidgets.QTabWidget(MainWindow)
        self.tabWidget.setGeometry(QtCore.QRect(40, 20, 1300, 850))
        self.tabWidget.setStyleSheet("style\n" "rgb(255, 255, 127)")
        self.tabWidget.setObjectName("tabWidget")
        
        #tab안에 들어갈 object들 정의
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("Home_tab")
        
        #FileButton Ui
        self.FileButton = QtWidgets.QPushButton(self.tab)
        self.FileButton.setGeometry(QtCore.QRect(200, 80, 90, 30))
        self.FileButton.setObjectName("FileButton")
        
        #FileInfo Ui
        self.FileInfoWidget = QtWidgets.QTreeWidget(self.tab) # home의 widget
        self.FileInfoWidget.setGeometry(QtCore.QRect(200, 120, 800, 600))
        self.FileInfoWidget.setObjectName("FileInfoWidget")
        
        #qtreewidget의 옵션들이 굉장히 많다. 여기서 잘 조합하면 treewidget 변경 가능.
        self.FileInfoWidget.setColumnCount(2)
        self.FileInfoWidget.setHeaderLabels(['property','value']) # property header

        
        self.tabWidget.addTab(self.tab, "")

        
        ##############tab_2 == Result
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        
        # groubox(Analyzed slot)
        self.groupBox = QtWidgets.QGroupBox(self.tab_2)
        self.groupBox.setGeometry(QtCore.QRect(250, 50, 1020, 750))
        self.groupBox.setObjectName("groupBox")
        
        
        # tablewidget = hex data widget
        self.tableWidget = QtWidgets.QTableWidget(self.groupBox)
        self.tableWidget.setGeometry(QtCore.QRect(20, 20, 1050, 571))
        self.tableWidget.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)


        
        self.tabWidget.addTab(self.tab_2, "")
        
    
        self.retranslateUi(MainWindow)
        #self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    
    
    def retranslateUi(self, MainWindow):        # ui -> 기능 연결점
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "NXFS"))
        
        
        self.FileButton.setText(_translate("Form", "File"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Home"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Result"))
        self.FileButton.clicked.connect(self.openfile_handler)
               
        self.groupBox.setTitle(_translate("MainWindow", "Analyzed"))
        
        
        
        

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    widget = QtWidgets.QWidget()
    ui = Ui_MainWindow()      #class로 정의한 UI Window
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
