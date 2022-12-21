
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QLineEdit, QCheckBox,QAction,qApp,QMenu, QDialogButtonBox, QMessageBox
import sys
import os, time
import sqlite3
import pandas as pd
from PyQt5.QtCore import pyqtSlot
from collections import defaultdict,OrderedDict
from tkinter import filedialog
import numpy
import sqquery
#import recovery_main

class Ui_MainWindow(object):
    
    def __init__(self):
        super().__init__()
        
        #os.system('"./dist/core.exe"')
        #os.system(os.getcwd()+"\dist\core.exe")
        #print(os.getcwd())
        
        
    
    def openfile_handler(self):     # file open dialog
        global path

        
        file = QFileDialog.getOpenFileName(widget, "Open Single File", "", "All Files(*)")
        path = file[0]
        print(path)
        
        #getcoreexe= os.path.realpath('..\\dist\\newcore\\newcore.exe ')      #.exe일때 돌아가는 코드(.exe 위치 기준으로 경로를 찾기 떄문)
        #print(getcoreexe)   #코어의 path경로
        #print(getcoreexe+path)
        
        os.system('newcore.exe -p ' + path )#+ )
        #os.system(getcoreexe )#+ path)   #path 인자 잘 넘어감 (파이썬 상)
        #os.system(getcoreexe + '{path}') #설마 이것도 .exe상? -> getcoreexe '{path}'로 나옴
    
        self.fileInfo()
        
        sqquery.csv_db()
        #sqquery.result_tab()
        
        
        
    
    def fileInfo(self):         # file information home page에 띄워주는 기능
        global path
        '''
        _translate = QtCore.QCoreApplication.translate
        
        
        meta = {'File': os.path.basename(path),
        'path': path.lstrip('.') , 
        'Created time': time.ctime(os.path.getctime(path)),
        'Modified time': time.ctime(os.path.getmtime(path)),
        'Access time': time.ctime(os.path.getatime(path)),
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
        '''
        #self.tabWidget.setCurrentIndex(1)  # 화면 전환 Home -> Assigned page
        self.ParsingF() 
    
    
    def assign_distriction(self):               #result page의 좌측상단 파일명 표기
        global path
        
        _translate = QtCore.QCoreApplication.translate
        f = os.path.basename(path)
        
        self.assignwidget.headerItem().setText(0, _translate("MainWindow", f))
        __sortingEnabled = self.assignwidget.isSortingEnabled()
    
    
    
    def ParsingF(self):                                             # hex parsing 함수
        global path
        

        #_translate = QtCore.QCoreApplication.translate
        #self.groupBox.setTitle(_translate("MainWindow", "Analyzed"))
        
        self.assign_distriction()
        #self.dbconnect()
        self.treewidget()
        
    
    def setupUi(self, MainWindow):
        
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1400, 900)
        MainWindow.setWindowIcon(QtGui.QIcon('main_logo.ico'))
        MainWindow.setWindowTitle(_translate("MainWindow", "NxFS Analyzer"))
        #--------------------------------------------------------------
        
        self.menubar = QtWidgets.QMenuBar(MainWindow) #rgb(49,49,49); 색깔 맘에듬.
        self.menubar.setStyleSheet("""
        QMenuBar {
            background-color: navy;    
            color: white;
            border: 1px solid navy;
            width: 50px;
        }

        QMenuBar::item {
            background-color: navy;
            color: white;
            width: 50px;
        }

        QMenuBar::item::selected {
            background-color: blue;
        }

        QMenu {
            background-color: white;
            color: navy;
            border: 1px solid navy;           
        }

        QMenu::item::selected {
            color: white;
            background-color: navy;
            
        }
    """)
        self.menubar.setGeometry(QtCore.QRect(300, 0, 1400, 0))
        self.menubar.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.menubar.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        self.menubar.setDefaultUp(False)
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        
        menu_file = self.menubar.addMenu(' File ')
        file_open = menu_file.addAction('&Open ')
        file_open.setShortcut('Ctrl+O')
        file_open.triggered.connect(self.openfile_handler)
        
        
        #menu_tool = self.menubar.addMenu(' Find ')
        menu_tool = self.menubar.addMenu(' Tool ')
        tool_find = menu_tool.addAction('&Find ')
        tool_find.setShortcut("Ctrl+F")
        tool_find.triggered.connect(self.searchui)
        
        
        
        
        tool_export = menu_tool.addAction('&Export ')
        tool_export.setShortcut("Ctrl+E")
        tool_export.triggered.connect(self.export_csvui)
        #tool_find = menu_tool.addAction('&Find ')
        #tool_find.setShortcut('Ctrl+F')
        #tool_find.triggered.connect(self.searchtext)
        #menu_tool.set
        
     
        
        
        #-------------------------------------------------------------
        
        self.tabWidget= QtWidgets.QTabWidget(MainWindow)  
        self.tabWidget.setStyleSheet("QTabWidget::pane {\n"
            "border-width: 2px;\n"
            "border-style: solid;\n"
            "border-color: navy;\n"
            "border-radius: 6px;\n"
            "}\n"
            
            "\n"
            "QTabBar::tab {\n"
            "background: white;\n"
            "color: red;\n"
            "border-width: 1px;\n"
            "border-style: solid;\n"
            "border-color: navy;\n"
            "border-bottom-color: navy;\n"
            "border-top-left-radius: 4px;\n"
            "border-top-right-radius: 4px;\n"
            "min-height: 30px;\n"
            #"padding: 5px;\n"
            "width: 100px;\n"
            "font: bold 14px;\n"
            "}"
            
            "\n"
            "QTabBar::tab:selected {\n"                            
            "border-color: navy;\n"
            #"font: bold 14px;\n"

            "background: navy;"                             
            "border-bottom-color: navy;\n"                
            "}\n"                   
            )
        self.tabWidget.setGeometry(QtCore.QRect(300, 80, 1050, 750))
        self.tabWidget.setObjectName("tabWidget")
        #self.tabwidget.tabBar().setTabTextColor(i, QColor(color))
        
        self.fileinfotab = QtWidgets.QWidget()   
        self.fileinfotab.setObjectName("fileinfotab")
        
        #FileInfo Ui                        
        #self.FileInfoWidget = QtWidgets.QTreeWidget(self.fileinfotab)
        #self.FileInfoWidget.setGeometry(QtCore.QRect(10, 15, 1020, 700))
        #self.FileInfoWidget.setObjectName("FileInfoWidget")
        #self.FileInfoWidget.setFrameShape(QtWidgets.QFrame.Box)
        #self.FileInfoWidget.setFrameShadow(QtWidgets.QFrame.Sunken)
        
       
        #self.FileInfoWidget.setColumnCount(2)
        #self.FileInfoWidget.setHeaderLabels(['property','value']) # property header
    
        #self.tabWidget.addTab(self.fileinfotab, "")
        
        
        self.resulttab = QtWidgets.QWidget()
        self.resulttab.setObjectName("resulttab")
        self.tabWidget.addTab(self.resulttab, "")
        
        
        #assgined/non-assigned treewidget
        self.assignwidget = QtWidgets.QTreeWidget(MainWindow) # home의 widget
        self.assignwidget.setStyleSheet(
            "QHeaderView::section {\n"
            "     background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
            "                                       stop:0 #616161, stop: 0.5 #505050,\n"
            "                                       stop: 0.6 #434343, stop:1 #656565);\n"
            "     color: white;\n"
            "     padding-left: 4px;\n"
            "     border: 1px solid navy;\n"
            " }\n"


        
            "QTreeview {            \n"
        "            border:2px solid rgb(67, 67, 70);\n"
        "            border-color: rgb(000, 000, 102);\n"
        "            color: navy;\n"
        "            border-radius:8px ; }\n")
        
            
            #("""
            #QHeaderView::section {                          
            #color: black;                               
            #padding: 2px;                               
            #height:20px;                                
            #border: 0px solid #567dbc;                  
            #border-left:0px;                            
            #border-right:0px;                           
            #background: #f9f9f9;                        
            #}
            #""")
        self.assignwidget.setGeometry(QtCore.QRect(30, 80, 250, 750))
        self.assignwidget.setObjectName("assignwidget")
        self.assignwidget.setFrameShape(QtWidgets.QFrame.Box)
        self.assignwidget.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.assignwidget.setHeaderHidden(True)
        
        
        
        # export_csv button
        self.exportcsvButton = QtWidgets.QPushButton(MainWindow)
        self.exportcsvButton.setStyleSheet(
            "background-color: rgb(000, 000, 102);\n"
            "border-style: outset;\n"
            "border-width: 2px;\n"
            "border-radius: 10px;\n"
            "border-color: white;\n"
            "font: bold 14px;\n"
            "color: white;\n"
            "min-width: 5em;\n"
            "padding: 6px;\n"
        )
        self.exportcsvButton.setGeometry(QtCore.QRect(158, 835, 122, 30))
        self.exportcsvButton.setObjectName("exportcsvbutton")
        _translate = QtCore.QCoreApplication.translate
        self.exportcsvButton.setText(_translate("Form", "Export_CSV"))
        self.exportcsvButton.clicked.connect(self.export_csvui)
        
        
        # export_avi button
        self.exportaviButton = QtWidgets.QPushButton(MainWindow)
        self.exportaviButton.setStyleSheet(
            "background-color: rgb(000, 000, 102);\n"
            "border-style: outset;\n"
            "border-width: 2px;\n"
            "border-radius: 10px;\n"
            "border-color: white;\n"
            "font: bold 14px;\n"
            "color: white;\n"
            "min-width: 5em;\n"
            "padding: 6px;\n"
        )
        self.exportaviButton.setGeometry(QtCore.QRect(29, 835, 122, 30))
        self.exportaviButton.setObjectName("exportaviButton")
        _translate = QtCore.QCoreApplication.translate
        self.exportaviButton.setText(_translate("Form", "Export"))
        self.exportaviButton.clicked.connect(self.export_avi)


        
        
        
        
        
        
        # tablewidget
        self.tableWidget = QtWidgets.QTableWidget(self.resulttab)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, 1045, 725))
        self.tableWidget.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget.verticalHeader().sectionClicked.connect(self.transhex)
        
        '''        
        #selectAll button?
        _translate = QtCore.QCoreApplication.translate
        self.selectbutton = QtWidgets.QPushButton(self.tab_2)
        self.selectbutton.setGeometry(QtCore.QRect(297, 80, 19, 20))
        self.selectbutton.setObjectName("selectAll")
        '''
        
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        #self.tabWidget.setTabText(self.tabWidget.indexOf(self.fileinfotab), _translate("MainWindow", "File Info"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.resulttab), _translate("MainWindow", "Result"))
        
        self.assignwidget.itemClicked.connect(self.treeitemClick)
        
        self.tableWidget.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.ActionsContextMenu)
        hash = QAction("Hash Calculation",self.tableWidget)
        self.tableWidget.addAction(hash)
        
        hash.triggered.connect(self.hashcal)
        
        
        
        
        
    def treewidget(self):
        conn = sqlite3.connect(os.path.realpath('NxFS_final.db'),isolation_level=None)  
        c = conn.cursor()
        
        #find all of table names
        c.execute("SELECT tbl_name FROM sqlite_master")
        a = c.fetchall()
        #c.execute("SELECT distinct replace(substr (datetime,0,11),'-','') from ALLOCATION group by datetime")
        #b = c.fetchall()
        
        _translate = QtCore.QCoreApplication.translate
        
        tablelist = []
        
        #datetime = []
        #toplevelitem list parsing with sqlite table names 
        
        for i in a:
            tablelist.append(i[0])      #ALLOCATION, UNALLOCATION, SLACK
        
        #for j in b:
        #    datetime.append(j[0])
        #print(tablelist,datetime)    #tablelist = 최상위 폴더, datetime = ALLOCATION의 날짜
        
        
        num = 0
        
        while num< len(tablelist):
            item_0 = QtWidgets.QTreeWidgetItem(self.assignwidget)
            self.assignwidget.topLevelItem(num).setText(0, _translate("MainWindow", tablelist[num]))
            
            num+=1
        
        self.assignwidget.setHeaderHidden(False)
        #while num<len(datetime):
            #if res[num][1] == '0':
            #    pass
            #else:
            #    item_1 = QtWidgets.QTreeWidgetItem(item_0)
            #    self.assignwidget.topLevelItem(num).child(0).setText(0, _translate("MainWindow", res[num][1]))
            #num+=1      
        
    
        
    # qtreewidget 항목 클릭시, 해당 항목의 조회 query를 db로 보냄
    def treeitemClick(self):
        global query
        global treeclickvalue
        
        self.tabWidget.setCurrentIndex(1)
        
        treeitem = self.assignwidget.selectedItems()
        
        for it in treeitem: 
            treeclickvalue = it.text(0)   # type == class

        
        if treeclickvalue == 'ALLOCATION':
            query = "SELECT name,start_offset,end_offset,size,datetime,folder,folder_index FROM " + treeclickvalue   #treeclickvalue = clicked treewidget text return .
        else:
            pass
        
        if treeclickvalue == 'UNALLOCATION':
            query = "SELECT start_offset, end_offset, size, folder, folder_index FROM " + treeclickvalue
        else:
            pass
            
        if treeclickvalue == 'SLACK':
            query = "SELECT name, start_offset, end_offset, size, folder FROM " +treeclickvalue
        else:
            pass    

        
        self.usingdb()
        
        
    def searchui(self):
        self.searchWidget = QtWidgets.QLineEdit(MainWindow)
        self.searchWidget.setStyleSheet(                        #lineedit(search widget) stylesheet
            "border:2px solid rgb(67, 67, 70);\n"
            "border-color: rgb(000, 000, 102);\n"
            "color: navy;\n"
            "border-radius:8px")
        self.searchWidget.setGeometry(QtCore.QRect(980, 70, 368, 28))
        self.searchWidget.setObjectName("searchWidget")
        self.searchWidget.setPlaceholderText("Input text and pressed enter..")
        self.searchWidget.setClearButtonEnabled(True)
        
        self.searchWidget.show()    
        
        self.searchWidget.returnPressed.connect(self.searchtext)
        
        
    # search bar에 text input시, 조회 query db에 보냄 
    def searchtext(self):
        global query
        #global texttodb
        global treeclickvalue
        global columnlist
        
        word = self.searchWidget.text().lower()

        if word:
            '''
            if('0x' in word):
                
                # 오프셋 값 속하는 부분 출력
                #print(hex(word))
                for row in range(self.tableWidget.rowCount()):
                    sOffset = int(self.tableWidget.item(row, 2).text(), 16)
                    eOffset = int(self.tableWidget.item(row, 3).text(), 16)
                    if(int(word, 16) <= eOffset & int(word, 16) >= sOffset):
                        match = True
                self.tableWidget.setRowHidden(row, not match)
                

            else:
            '''
            for row in range(self.tableWidget.rowCount()):
                match = False
                for col in range(self.tableWidget.columnCount()):
                    item = self.tableWidget.item(row, col)
                    if item is not None and word in item.text().lower():
                        match = True
                        break
                self.tableWidget.setRowHidden(row, not match)
        else:
            for i in range(self.tableWidget.rowCount()):
                self.tableWidget.setRowHidden(i, False)
        #self.searchWidget.returnPressed.connect(self.searchtext)
        #print(columnlist)
        """
        texttodb = self.searchWidget.text()   #input text 내용 가져옴
        try:
            i=1
            w=''
            while i<len(columnlist):
                print(columnlist[i]) 
            
                w += columnlist[i]+'||'+"' '||" 
                
            
                i+=1
            w += "''"           #2 12 도 검색되는 버그 해결
            
            #print(w)
            query = '''SELECT * FROM ''' +treeclickvalue+ ''' WHERE (''' + w + ''') LIKE '''+ '"%' + texttodb + '%"'
            self.usingdb()
        except NameError:       # 빈화면에 find시 에러 exception
            pass
            
        #print(query)
        """
        
        
        
    # query를 받아 db 동작함
    def usingdb(self):
        global query
        #global texttodb
        global a
        global getrow
        global treeclickvalue
        global columnlist
        #conn = sqlite3.connect(os.path.realpath('./NxFS_final.db'),isolation_level=None)       #exe화 시 경로 맞음!
        #c = conn.cursor()
        
        #sqquery.result_tab()
        n= 1
        
        #result_tab_ALLOCATION = "select name,start_offset,end_offset,size,datetime,folder_index from ALLOCATION"
        #sqquery.c.execute(result_tab_ALLOCATION)
        #ALLOCTION= sqquery.c.fetchall()
        #result_tab_UNALLOCATION = "select start_offset,end_offset,size,folder,folder_index from UNALLOCATION"
        #sqquery.c.execute(result_tab_UNALLOCATION)
        #UNALLOCTION = sqquery.c.fetchall()
        #result_tab_SLACK = "select * from slack"
        #sqquery.c.execute(result_tab_SLACK)
        #UNALLOCTION = sqquery.c.fetchall()
        #sqquery.c.connection.commit()
        
        #sqquery.c.execute("SELECT EXISTS (" +query+")")
        sqquery.c.execute("SELECT EXISTS (" +query+")")
        find = sqquery.c.fetchall()
        #print(find)
        #print(find)
        #a = sqquery.c.fetchall()
        #print(a)
        
        if treeclickvalue == 'ALLOCATION':
        
        #sqquery.c.execute("select name,start_offset,end_offset,size,datetime,folder,folder_index from "+treeclickvalue)   #-------> it's working
        #column = sqquery.c.fetchall()
        #print(column)
        
            self.tableWidget.setColumnCount(8)  #column count and make
        
            columnlist = ['','NAME','START_OFFSET','END_OFFSET','SIZE','DATETIME(UTC)','FOLDER','FOLDER_INDEX']            #get column names
            #for i in column:
            #    columnlist.append(i[1])
        
        
            self.tableWidget.setHorizontalHeaderLabels(columnlist)  #set column header in tablewidget
        
        elif treeclickvalue == 'UNALLOCATION':
            self.tableWidget.setColumnCount(6)  #column count and make
        
            columnlist = ['','START_OFFSET','END_OFFSET','SIZE','FOLDER','FOLDER_INDEX']
            self.tableWidget.setHorizontalHeaderLabels(columnlist)
        
        elif treeclickvalue == 'SLACK':
            self.tableWidget.setColumnCount(6)  #column count and make
        
            columnlist = ['','NAME', 'START_OFFSET','END_OFFSET','SIZE','FOLDER']
            self.tableWidget.setHorizontalHeaderLabels(columnlist)
        
        
        
        
        #self.tableWidget.setHorizontalHeaderLabels(['','File_Name', 'Start_Offset', 'End_Offset', 'Created time', 'Size', 'MD5','SHA-1','SHA-256'])
        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(20)
        self.tableWidget.setColumnWidth(0,25)
        
        #self.tableWidget.horizontalHeader().icon
        
        #self.tableWidget.itemClicked.connect(self.chkclicked)
        #self.tableWidget.setColumnWidth(1,200)
        #self.tableWidget.setColumnWidth(2,150)
        #self.tableWidget.setColumnWidth(3,150)
        #self.tableWidget.setColumnWidth(4,200)
        #self.tableWidget.setColumnWidth(5,150)
        #self.tableWidget.setColumnWidth(6,150)
        #self.tableWidget.setColumnWidth(7,150)
        #self.tableWidget.setColumnWidth(8,150)

        self.tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        #self.tableWidget.resizeColumnsToContents()
        
        
        tablerow = 0
        
        # 빈 query 조회시,
        if sqquery.c.fetchall() == [(0,)]: 
            self.tableWidget.setRowCount(0)
        
        #검색결과 일치 x 조회시,
        elif find == [(0,)]:
            self.tableWidget.setRowCount(0)
        #elif sqquery.c.execute("SELECT EXISTS (" +query+")") :
        #    print(sqquery.c.fetchall())
        
        # 결과값이 있는 query 조회시,
        else:
            for row in sqquery.c.execute(query):
                
                #print(query)

                if "%%" in query:
                    self.tableWidget.setRowCount(0)

                
                else:
                    
                    self.tableWidget.setRowCount(n)
                    #item.setCheckState(QtCore.Qt.Checked)
                    #item = QtWidgets.QTableWidgetItem()
                    #item.setCheckState(QtCore.Qt.Unchecked)  # unchecked == 0 , checked == 2 값을 가짐.
                    ############이거 안됨. 바꾸자 221126 
                    #self.tableWidget.setItem(tablerow, 0, item)
                    
                    a = QtWidgets.QCheckBox()
                    self.tableWidget.setCellWidget(tablerow,0,a)
                    a.stateChanged.connect(self.chkclicked)
                    
                    global result
                    result = []
                    
                    getrow = defaultdict(list)
                    
                    for i in range(len(columnlist)-1):
                        self.tableWidget.setItem(tablerow, i+1, QtWidgets.QTableWidgetItem(row[i]))
                        #self.tableWidget.item(tablerow,i+1).setTextAlignment(QtCore.Qt.AlignCenter)
                    
                    
                            

                    
                    tablerow +=1
                    n+=1
        
        
        
        
    
    
    def hashcal(self):
        global path
        
        if treeclickvalue == 'ALLOCATION':
            clickrow = self.tableWidget.currentItem().row()
            
            aviargv = self.tableWidget.item(clickrow,7).text()  #클릭한 줄에 있는 폴더 인덱스값 가져옴.
            
            hashargv = 'newcore.exe -p ' + path + ' -ha ' + aviargv 
            print(hashargv)
            
            
            get = os.popen(hashargv).readlines()
            hashes = get[-4:-1]
            get=[]
            
            for i in hashes:
                strip = i.strip()
                get.append(strip)
            #print(get)             # hash 값 추출
            
            
            
            Dialog = QtWidgets.QDialog(MainWindow)
            Dialog.setObjectName("hashDialog")
            Dialog.resize(516, 464)
            self.pushButton = QtWidgets.QPushButton(Dialog)
            self.pushButton.setGeometry(QtCore.QRect(160, 410, 131, 28))
            self.pushButton.setObjectName("pushButton")
            #self.pushButton.clicked.connect(self.ok)
            self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
            self.groupBox_2.setGeometry(QtCore.QRect(30, 40, 461, 351))
            self.groupBox_2.setObjectName("groupBox_2")
            self.formLayoutWidget = QtWidgets.QWidget(self.groupBox_2)
            self.formLayoutWidget.setGeometry(QtCore.QRect(10, 20, 421, 311))
            self.formLayoutWidget.setObjectName("formLayoutWidget")
            self.verticalLayout = QtWidgets.QVBoxLayout(self.formLayoutWidget)
            self.verticalLayout.setContentsMargins(0, 0, 0, 0)
            self.verticalLayout.setObjectName("verticalLayout")
            
            self.MD5 = QtWidgets.QLabel(self.formLayoutWidget)
            self.MD5.setObjectName("MD5")
            self.verticalLayout.addWidget(self.MD5)
            #self.MD5.setText("Test set Text") #텍스트 변환
            self.MD5.setFont(QtGui.QFont("",12)) #폰트,크기 조절
            self.MD5.setStyleSheet("Color : navy") #글자색 변환
            self.MD5Value = QtWidgets.QLabel(self.formLayoutWidget)
            self.MD5Value.setObjectName("MD5Value")
            self.verticalLayout.addWidget(self.MD5Value)
            self.SHA1 = QtWidgets.QLabel(self.formLayoutWidget)
            self.SHA1.setObjectName("SHA1")
            self.verticalLayout.addWidget(self.SHA1)
            self.SHA1.setFont(QtGui.QFont("",12)) #폰트,크기 조절
            self.SHA1.setStyleSheet("Color : navy") #글자색 변환
            self.SHA1Value = QtWidgets.QLabel(self.formLayoutWidget)
            self.SHA1Value.setObjectName("SHA1Value")
            self.verticalLayout.addWidget(self.SHA1Value)
            self.SHA256 = QtWidgets.QLabel(self.formLayoutWidget)
            self.SHA256.setObjectName("SHA256")
            self.verticalLayout.addWidget(self.SHA256)
            self.SHA256.setFont(QtGui.QFont("",12)) #폰트,크기 조절
            self.SHA256.setStyleSheet("Color : navy") #글자색 변환
            self.SHA256Value = QtWidgets.QLabel(self.formLayoutWidget)
            self.SHA256Value.setObjectName("SHA256Value")
            self.verticalLayout.addWidget(self.SHA256Value)
            
            self.MD5Value.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
            self.SHA1Value.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
            self.SHA256Value.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)

            QtCore.QMetaObject.connectSlotsByName(Dialog)


            _translate = QtCore.QCoreApplication.translate
            Dialog.setWindowTitle(_translate("Dialog", "Hash calculation"))
            self.pushButton.setText(_translate("Dialog", "OK"))
            self.groupBox_2.setTitle(_translate("Dialog", "Hash"))
            self.MD5.setText(_translate("Dialog", "MD5"))
            self.MD5Value.setText(_translate("Dialog", get[0]))
            self.SHA1.setText(_translate("Dialog", "SHA1"))
            self.SHA1Value.setText(_translate("Dialog", get[1]))
            self.SHA256.setText(_translate("Dialog", "SHA256"))
            self.SHA256Value.setText(_translate("Dialog", get[2]))

            Dialog.show()
            
        #------------------------------------------------------------------
        if treeclickvalue == 'UNALLOCATION':
            clickrow = self.tableWidget.currentItem().row()
            
            aviargv = self.tableWidget.item(clickrow,5).text()  #클릭한 줄에 있는 폴더 인덱스값 가져옴.
            
            hashargv = 'newcore.exe -p ' + path + ' -ha ' + aviargv 
            print(hashargv)
            
            
            get = os.popen(hashargv).readlines()
            hashes = get[-4:-1]
            get=[]
            
            for i in hashes:
                strip = i.strip()
                get.append(strip)
            #print(get)             # hash 값 추출
            
            
            
            Dialog = QtWidgets.QDialog(MainWindow)
            Dialog.setObjectName("hashDialog")
            Dialog.resize(516, 464)
            self.pushButton = QtWidgets.QPushButton(Dialog)
            self.pushButton.setGeometry(QtCore.QRect(160, 410, 131, 28))
            self.pushButton.setObjectName("pushButton")
            #self.pushButton.clicked.connect(self.ok)
            self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
            self.groupBox_2.setGeometry(QtCore.QRect(30, 40, 461, 351))
            self.groupBox_2.setObjectName("groupBox_2")
            self.formLayoutWidget = QtWidgets.QWidget(self.groupBox_2)
            self.formLayoutWidget.setGeometry(QtCore.QRect(10, 20, 421, 311))
            self.formLayoutWidget.setObjectName("formLayoutWidget")
            self.verticalLayout = QtWidgets.QVBoxLayout(self.formLayoutWidget)
            self.verticalLayout.setContentsMargins(0, 0, 0, 0)
            self.verticalLayout.setObjectName("verticalLayout")
            
            self.MD5 = QtWidgets.QLabel(self.formLayoutWidget)
            self.MD5.setObjectName("MD5")
            self.verticalLayout.addWidget(self.MD5)
            #self.MD5.setText("Test set Text") #텍스트 변환
            self.MD5.setFont(QtGui.QFont("",12)) #폰트,크기 조절
            self.MD5.setStyleSheet("Color : navy") #글자색 변환
            self.MD5Value = QtWidgets.QLabel(self.formLayoutWidget)
            self.MD5Value.setObjectName("MD5Value")
            self.verticalLayout.addWidget(self.MD5Value)
            self.SHA1 = QtWidgets.QLabel(self.formLayoutWidget)
            self.SHA1.setObjectName("SHA1")
            self.verticalLayout.addWidget(self.SHA1)
            self.SHA1.setFont(QtGui.QFont("",12)) #폰트,크기 조절
            self.SHA1.setStyleSheet("Color : navy") #글자색 변환
            self.SHA1Value = QtWidgets.QLabel(self.formLayoutWidget)
            self.SHA1Value.setObjectName("SHA1Value")
            self.verticalLayout.addWidget(self.SHA1Value)
            self.SHA256 = QtWidgets.QLabel(self.formLayoutWidget)
            self.SHA256.setObjectName("SHA256")
            self.verticalLayout.addWidget(self.SHA256)
            self.SHA256.setFont(QtGui.QFont("",12)) #폰트,크기 조절
            self.SHA256.setStyleSheet("Color : navy") #글자색 변환
            self.SHA256Value = QtWidgets.QLabel(self.formLayoutWidget)
            self.SHA256Value.setObjectName("SHA256Value")
            self.verticalLayout.addWidget(self.SHA256Value)
            
            self.MD5Value.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
            self.SHA1Value.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
            self.SHA256Value.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)

            QtCore.QMetaObject.connectSlotsByName(Dialog)


            _translate = QtCore.QCoreApplication.translate
            Dialog.setWindowTitle(_translate("Dialog", "Hash calculation"))
            self.pushButton.setText(_translate("Dialog", "OK"))
            self.groupBox_2.setTitle(_translate("Dialog", "Hash"))
            self.MD5.setText(_translate("Dialog", "MD5"))
            self.MD5Value.setText(_translate("Dialog", get[0]))
            self.SHA1.setText(_translate("Dialog", "SHA1"))
            self.SHA1Value.setText(_translate("Dialog", get[1]))
            self.SHA256.setText(_translate("Dialog", "SHA256"))
            self.SHA256Value.setText(_translate("Dialog", get[2]))

            Dialog.show()
        
        if treeclickvalue == 'SLACK':
            clickrow = self.tableWidget.currentItem().row()
            
            aviargv = self.tableWidget.item(clickrow,1).text()  #클릭한 줄에 있는 폴더 인덱스값 가져옴.
            
            hashargv = 'newcore.exe -p ' + path + ' -hs ' + aviargv 
            print(hashargv)
            
            #test
            
            get = os.popen(hashargv).readlines()
            hashes = get[-4:-1]
            get=[]
            
            for i in hashes:
                strip = i.strip()
                get.append(strip)
            #print(get)             # hash 값 추출
            
            
            
            Dialog = QtWidgets.QDialog(MainWindow)
            Dialog.setObjectName("hashDialog")
            Dialog.resize(516, 464)
            self.pushButton = QtWidgets.QPushButton(Dialog)
            self.pushButton.setGeometry(QtCore.QRect(160, 410, 131, 28))
            self.pushButton.setObjectName("pushButton")
            #self.pushButton.clicked.connect(self.ok)
            self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
            self.groupBox_2.setGeometry(QtCore.QRect(30, 40, 461, 351))
            self.groupBox_2.setObjectName("groupBox_2")
            self.formLayoutWidget = QtWidgets.QWidget(self.groupBox_2)
            self.formLayoutWidget.setGeometry(QtCore.QRect(10, 20, 421, 311))
            self.formLayoutWidget.setObjectName("formLayoutWidget")
            self.verticalLayout = QtWidgets.QVBoxLayout(self.formLayoutWidget)
            self.verticalLayout.setContentsMargins(0, 0, 0, 0)
            self.verticalLayout.setObjectName("verticalLayout")
            
            self.MD5 = QtWidgets.QLabel(self.formLayoutWidget)
            self.MD5.setObjectName("MD5")
            self.verticalLayout.addWidget(self.MD5)
            #self.MD5.setText("Test set Text") #텍스트 변환
            self.MD5.setFont(QtGui.QFont("",12)) #폰트,크기 조절
            self.MD5.setStyleSheet("Color : navy") #글자색 변환
            self.MD5Value = QtWidgets.QLabel(self.formLayoutWidget)
            self.MD5Value.setObjectName("MD5Value")
            self.verticalLayout.addWidget(self.MD5Value)
            self.SHA1 = QtWidgets.QLabel(self.formLayoutWidget)
            self.SHA1.setObjectName("SHA1")
            self.verticalLayout.addWidget(self.SHA1)
            self.SHA1.setFont(QtGui.QFont("",12)) #폰트,크기 조절
            self.SHA1.setStyleSheet("Color : navy") #글자색 변환
            self.SHA1Value = QtWidgets.QLabel(self.formLayoutWidget)
            self.SHA1Value.setObjectName("SHA1Value")
            self.verticalLayout.addWidget(self.SHA1Value)
            self.SHA256 = QtWidgets.QLabel(self.formLayoutWidget)
            self.SHA256.setObjectName("SHA256")
            self.verticalLayout.addWidget(self.SHA256)
            self.SHA256.setFont(QtGui.QFont("",12)) #폰트,크기 조절
            self.SHA256.setStyleSheet("Color : navy") #글자색 변환
            self.SHA256Value = QtWidgets.QLabel(self.formLayoutWidget)
            self.SHA256Value.setObjectName("SHA256Value")
            self.verticalLayout.addWidget(self.SHA256Value)
            
            self.MD5Value.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
            self.SHA1Value.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
            self.SHA256Value.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)

            QtCore.QMetaObject.connectSlotsByName(Dialog)


            _translate = QtCore.QCoreApplication.translate
            Dialog.setWindowTitle(_translate("Dialog", "Hash calculation"))
            self.pushButton.setText(_translate("Dialog", "OK"))
            self.groupBox_2.setTitle(_translate("Dialog", "Hash"))
            self.MD5.setText(_translate("Dialog", "MD5"))
            self.MD5Value.setText(_translate("Dialog", get[0]))
            self.SHA1.setText(_translate("Dialog", "SHA1"))
            self.SHA1Value.setText(_translate("Dialog", get[1]))
            self.SHA256.setText(_translate("Dialog", "SHA256"))
            self.SHA256Value.setText(_translate("Dialog", get[2]))

            Dialog.show()
        
        
    #def ok(self):
        #self.dialogclose()
                  
                  
                  
    def transhex(self):
            
        if '0x' in self.tableWidget.item(0,2).text():
            try:
                for i in range(self.tableWidget.rowCount()):
                    a = self.tableWidget.item(i,2).text()
                    b = self.tableWidget.item(i,3).text()
                #self.tableWidget.setItem(i,2,QtWidgets.QTableWidgetItem(hashlib.md5(a).hexdigest()))
                    deca = int(a,16)
                    decb = int(b,16)
                    
                    self.tableWidget.setItem(i,2,QtWidgets.QTableWidgetItem(str(deca)))
                    self.tableWidget.setItem(i,3,QtWidgets.QTableWidgetItem(str(decb)))
            except:
                pass
    
        else:
            for i in range(self.tableWidget.rowCount()):
                c = self.tableWidget.item(i,2).text()
                d = self.tableWidget.item(i,3).text()
                self.tableWidget.setItem(i,2,QtWidgets.QTableWidgetItem(str(hex(int(c)))))
                self.tableWidget.setItem(i,3,QtWidgets.QTableWidgetItem(str(hex(int(d)))))
  
        
    
    def chkclicked(self,state):        ### 클릭된 체크박스의 row 가져오기
        #global a
        global getrow
        #global rownum
        global result
        
        
        rownum = self.tableWidget.currentRow()  #table 재정렬해도 맞게 나옴.
        #print(rownum)
        
        
        
        
        #[dict ver.]  ERROR : 선택후 재정렬을 해버린 상태로 click 취소시 keyerror 발생. exception 해도 뭔가 엉성함.
        
        
        

        if state == 2:
            
            
            val = []
            
            for i in range(len(columnlist[1:])):
                #if self.tableWidget.item(rownum,i+1).text() not in val:
                    
                val.append(self.tableWidget.item(rownum,i+1).text())
            
                #print(val)
            
            result.append(val)
            result.sort()
            #print(result)
            #getrow[rownum] = val
            #result = dict(sorted(getrow.items()))
            #rint(result)
            
            
        else:
            re = []
            
            for i in range(len(columnlist[1:])):
                re.append(self.tableWidget.item(rownum,i+1).text())
                if re in result:
                    result.remove(re)
            #del(getrow[rownum])
            #result = dict(sorted(getrow.items()))
        
        #print(result)
        #print(columnlist)

        
            
    def export_csvui(self):
        global result
        
        try:
            if treeclickvalue == 'ALLOCATION':
                Dialog = QtWidgets.QDialog(MainWindow)
                
                Dialog.setObjectName("Dialog")
                Dialog.resize(442, 625)
                self.pushButton = QtWidgets.QPushButton(Dialog)
                self.pushButton.setGeometry(QtCore.QRect(160, 530, 131, 28))
                self.pushButton.setObjectName("pushButton")
                self.groupBox = QtWidgets.QGroupBox(Dialog)
                self.groupBox.setGeometry(QtCore.QRect(40, 30, 361, 291))
                self.groupBox.setObjectName("groupBox")
                self.verticalLayoutWidget = QtWidgets.QWidget(self.groupBox)
                self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 20, 341, 271))
                self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
                self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
                self.verticalLayout.setContentsMargins(0, 0, 0, 0)
                self.verticalLayout.setObjectName("verticalLayout")
                self.FILE_NAME = QtWidgets.QCheckBox(self.verticalLayoutWidget)
                self.FILE_NAME.setObjectName("FILE_NAME")
                self.verticalLayout.addWidget(self.FILE_NAME)
                self.START_OFFSET = QtWidgets.QCheckBox(self.verticalLayoutWidget)
                self.START_OFFSET.setObjectName("START_OFFSET")
                self.verticalLayout.addWidget(self.START_OFFSET)
                self.END_OFFSET = QtWidgets.QCheckBox(self.verticalLayoutWidget)
                self.END_OFFSET.setObjectName("END_OFFSET")
                self.verticalLayout.addWidget(self.END_OFFSET)
                self.FILE_SIZE = QtWidgets.QCheckBox(self.verticalLayoutWidget)
                self.FILE_SIZE.setObjectName("FILE_SIZE")
                self.verticalLayout.addWidget(self.FILE_SIZE)
                self.DATETIME = QtWidgets.QCheckBox(self.verticalLayoutWidget)
                self.DATETIME.setObjectName("DATETIME")
                self.verticalLayout.addWidget(self.DATETIME)
                self.FOLDER = QtWidgets.QCheckBox(self.verticalLayoutWidget)
                self.FOLDER.setObjectName("FOLDER")
                self.verticalLayout.addWidget(self.FOLDER)
                self.FOLDER_INDEX = QtWidgets.QCheckBox(self.verticalLayoutWidget)
                self.FOLDER_INDEX.setObjectName("FOLDER_INDEX")
                self.verticalLayout.addWidget(self.FOLDER_INDEX)
                self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
                self.groupBox_2.setGeometry(QtCore.QRect(40, 340, 361, 161))
                self.groupBox_2.setObjectName("groupBox_2")
                self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.groupBox_2)
                self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(20, 20, 341, 141))
                self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
                self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
                self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
                self.verticalLayout_2.setObjectName("verticalLayout_2")
                self.MD5 = QtWidgets.QCheckBox(self.verticalLayoutWidget_2)
                self.MD5.setObjectName("MD5")
                self.verticalLayout_2.addWidget(self.MD5)
                self.SHA1 = QtWidgets.QCheckBox(self.verticalLayoutWidget_2)
                self.SHA1.setObjectName("SHA1")
                self.verticalLayout_2.addWidget(self.SHA1)
                self.SHA256 = QtWidgets.QCheckBox(self.verticalLayoutWidget_2)
                self.SHA256.setObjectName("SHA256")
                self.verticalLayout_2.addWidget(self.SHA256)

                _translate = QtCore.QCoreApplication.translate
                Dialog.setWindowTitle(_translate("Dialog", "Export_CSV"))
                self.pushButton.setText(_translate("Dialog", "Export"))
                self.groupBox.setTitle(_translate("Dialog", "Property"))
                self.FILE_NAME.setText(_translate("Dialog", "FILE_NAME"))
                self.START_OFFSET.setText(_translate("Dialog", "START_OFFSET"))
                self.END_OFFSET.setText(_translate("Dialog", "END_OFFSET"))
                self.FILE_SIZE.setText(_translate("Dialog", "FILE_SIZE"))
                self.DATETIME.setText(_translate("Dialog", "DATETIME"))
                self.FOLDER.setText(_translate("Dialog", "FOLDER"))
                self.FOLDER_INDEX.setText(_translate("Dialog", "FOLDER_INDEX"))
                self.groupBox_2.setTitle(_translate("Dialog", "Hash"))
                self.MD5.setText(_translate("Dialog", "MD5"))
                self.SHA1.setText(_translate("Dialog", "SHA-1"))
                self.SHA256.setText(_translate("Dialog", "SHA-256"))
                
                

                Dialog.show()

                
                self.pushButton.clicked.connect(self.export_csv)
                #print(result[0])
            
            elif treeclickvalue == 'UNALLOCATION':
                
                Dialog = QtWidgets.QDialog(MainWindow)
                
                Dialog.setObjectName("Dialog")
                Dialog.resize(442, 625)
                self.pushButton = QtWidgets.QPushButton(Dialog)
                self.pushButton.setGeometry(QtCore.QRect(160, 530, 131, 28))
                self.pushButton.setObjectName("pushButton")
                self.groupBox = QtWidgets.QGroupBox(Dialog)
                self.groupBox.setGeometry(QtCore.QRect(40, 30, 361, 291))
                self.groupBox.setObjectName("groupBox")
                self.verticalLayoutWidget = QtWidgets.QWidget(self.groupBox)
                self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 20, 341, 271))
                self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
                self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
                self.verticalLayout.setContentsMargins(0, 0, 0, 0)
                self.verticalLayout.setObjectName("verticalLayout")
                self.START_OFFSET = QtWidgets.QCheckBox(self.verticalLayoutWidget)
                self.START_OFFSET.setObjectName("START_OFFSET")
                self.verticalLayout.addWidget(self.START_OFFSET)
                self.END_OFFSET = QtWidgets.QCheckBox(self.verticalLayoutWidget)
                self.END_OFFSET.setObjectName("END_OFFSET")
                self.verticalLayout.addWidget(self.END_OFFSET)
                self.FILE_SIZE = QtWidgets.QCheckBox(self.verticalLayoutWidget)
                self.FILE_SIZE.setObjectName("FILE_SIZE")
                self.verticalLayout.addWidget(self.FILE_SIZE)
                self.FOLDER = QtWidgets.QCheckBox(self.verticalLayoutWidget)
                self.FOLDER.setObjectName("FOLDER")
                self.verticalLayout.addWidget(self.FOLDER)
                self.FOLDER_INDEX = QtWidgets.QCheckBox(self.verticalLayoutWidget)
                self.FOLDER_INDEX.setObjectName("FOLDER_INDEX")
                self.verticalLayout.addWidget(self.FOLDER_INDEX)
                self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
                self.groupBox_2.setGeometry(QtCore.QRect(40, 340, 361, 161))
                self.groupBox_2.setObjectName("groupBox_2")
                self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.groupBox_2)
                self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(20, 20, 341, 141))
                self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
                self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
                self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
                self.verticalLayout_2.setObjectName("verticalLayout_2")
                self.MD5 = QtWidgets.QCheckBox(self.verticalLayoutWidget_2)
                self.MD5.setObjectName("MD5")
                self.verticalLayout_2.addWidget(self.MD5)
                self.SHA1 = QtWidgets.QCheckBox(self.verticalLayoutWidget_2)
                self.SHA1.setObjectName("SHA1")
                self.verticalLayout_2.addWidget(self.SHA1)
                self.SHA256 = QtWidgets.QCheckBox(self.verticalLayoutWidget_2)
                self.SHA256.setObjectName("SHA256")
                self.verticalLayout_2.addWidget(self.SHA256)

                _translate = QtCore.QCoreApplication.translate
                Dialog.setWindowTitle(_translate("Dialog", "Export_CSV"))
                self.pushButton.setText(_translate("Dialog", "Export"))
                self.groupBox.setTitle(_translate("Dialog", "Property"))
                self.START_OFFSET.setText(_translate("Dialog", "START_OFFSET"))
                self.END_OFFSET.setText(_translate("Dialog", "END_OFFSET"))
                self.FILE_SIZE.setText(_translate("Dialog", "FILE_SIZE"))
                self.FOLDER.setText(_translate("Dialog", "FOLDER"))
                self.FOLDER_INDEX.setText(_translate("Dialog", "FOLDER_INDEX"))
                self.groupBox_2.setTitle(_translate("Dialog", "Hash"))
                self.MD5.setText(_translate("Dialog", "MD5"))
                self.SHA1.setText(_translate("Dialog", "SHA-1"))
                self.SHA256.setText(_translate("Dialog", "SHA-256"))
                
                

                Dialog.show()

                
                self.pushButton.clicked.connect(self.export_csv)
                
                
            elif treeclickvalue == 'SLACK':

                Dialog = QtWidgets.QDialog(MainWindow)
                
                Dialog.setObjectName("Dialog")
                Dialog.resize(442, 625)
                self.pushButton = QtWidgets.QPushButton(Dialog)
                self.pushButton.setGeometry(QtCore.QRect(160, 530, 131, 28))
                self.pushButton.setObjectName("pushButton")
                self.groupBox = QtWidgets.QGroupBox(Dialog)
                self.groupBox.setGeometry(QtCore.QRect(40, 30, 361, 291))
                self.groupBox.setObjectName("groupBox")
                self.verticalLayoutWidget = QtWidgets.QWidget(self.groupBox)
                self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 20, 341, 271))
                self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
                self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
                self.verticalLayout.setContentsMargins(0, 0, 0, 0)
                self.verticalLayout.setObjectName("verticalLayout")
                self.FILE_NAME = QtWidgets.QCheckBox(self.verticalLayoutWidget)
                self.FILE_NAME.setObjectName("FILE_NAME")
                self.verticalLayout.addWidget(self.FILE_NAME)
                self.START_OFFSET = QtWidgets.QCheckBox(self.verticalLayoutWidget)
                self.START_OFFSET.setObjectName("START_OFFSET")
                self.verticalLayout.addWidget(self.START_OFFSET)
                self.END_OFFSET = QtWidgets.QCheckBox(self.verticalLayoutWidget)
                self.END_OFFSET.setObjectName("END_OFFSET")
                self.verticalLayout.addWidget(self.END_OFFSET)
                self.FILE_SIZE = QtWidgets.QCheckBox(self.verticalLayoutWidget)
                self.FILE_SIZE.setObjectName("FILE_SIZE")
                self.verticalLayout.addWidget(self.FILE_SIZE)
                self.FOLDER = QtWidgets.QCheckBox(self.verticalLayoutWidget)
                self.FOLDER.setObjectName("FOLDER")
                self.verticalLayout.addWidget(self.FOLDER)
                self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
                self.groupBox_2.setGeometry(QtCore.QRect(40, 340, 361, 161))
                self.groupBox_2.setObjectName("groupBox_2")
                self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.groupBox_2)
                self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(20, 20, 341, 141))
                self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
                self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
                self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
                self.verticalLayout_2.setObjectName("verticalLayout_2")
                self.MD5 = QtWidgets.QCheckBox(self.verticalLayoutWidget_2)
                self.MD5.setObjectName("MD5")
                self.verticalLayout_2.addWidget(self.MD5)
                self.SHA1 = QtWidgets.QCheckBox(self.verticalLayoutWidget_2)
                self.SHA1.setObjectName("SHA1")
                self.verticalLayout_2.addWidget(self.SHA1)
                self.SHA256 = QtWidgets.QCheckBox(self.verticalLayoutWidget_2)
                self.SHA256.setObjectName("SHA256")
                self.verticalLayout_2.addWidget(self.SHA256)

                _translate = QtCore.QCoreApplication.translate
                Dialog.setWindowTitle(_translate("Dialog", "Export_CSV"))
                self.pushButton.setText(_translate("Dialog", "Export"))
                self.groupBox.setTitle(_translate("Dialog", "Property"))
                self.FILE_NAME.setText(_translate("Dialog", "FILE_NAME"))
                self.START_OFFSET.setText(_translate("Dialog", "START_OFFSET"))
                self.END_OFFSET.setText(_translate("Dialog", "END_OFFSET"))
                self.FILE_SIZE.setText(_translate("Dialog", "FILE_SIZE"))
                self.FOLDER.setText(_translate("Dialog", "FOLDER"))
                self.groupBox_2.setTitle(_translate("Dialog", "Hash"))
                self.MD5.setText(_translate("Dialog", "MD5"))
                self.SHA1.setText(_translate("Dialog", "SHA-1"))
                self.SHA256.setText(_translate("Dialog", "SHA-256"))
                
                

                Dialog.show()

                
                self.pushButton.clicked.connect(self.export_csv)
        except :
            pass
        
    
    
    def export_csv(self,state):
        global result
        global columnlist
        
        
        if treeclickvalue == 'ALLOCATION':
            
        
            a = self.FILE_NAME.isChecked()
            b = self.START_OFFSET.isChecked()
            c = self.END_OFFSET.isChecked()
            d = self.FILE_SIZE.isChecked()
            e = self.DATETIME.isChecked()
            f = self.FOLDER.isChecked()
            g = self.FOLDER_INDEX.isChecked()
            
            
        
       
            r = [a,b,c,d,e,f,g]
        
            
            array = numpy.array(r)
            #print(array)
            wh = numpy.where(array == True)     
            index = wh[0]       #선택한 항목의 인덱스 값
            
            
            df = []
            for i in result:
                for j in index:
                    df.append(i[j])
            
            dfslice = [df[i*len(index):(i+1)*len(index)] for i in range((len(df)-1+len(index))//len(index))]

            
            column = columnlist[1:]
            #col = column
            #result.update({"h" : })
            
            #print(index)
            #d = OrderedDict(index)  #헤더 추가해서 csv에 보여지게
            #d.move_to_end('h',last=False)
            #print(d)
            
            df2 = pd.DataFrame(dfslice)
            
            col = []
            for i in index:
                col.append(column[i])
                
            print(col)
            
            
            df2.columns = col
            

            #print(df)
            #df2 = df.drop(index)

            #reverse = df2.transpose()
            #reverse = df2.transpose() # 행/열 바꾸기
            print(df2)
            
            
            ftypes = [('csv file','.csv')]
            ftitle = 'Save as..'
            savefile = filedialog.asksaveasfilename(filetypes=ftypes, title=ftitle)  #save file 경로 리턴
            #print(savefile+'.csv')
            
            df2.to_csv(savefile+'.csv', index=False)    #csv로 저장!
                #reverse.to_csv('C:/Users/revib/OneDrive_hallym/바탕 화면/BOB/트랙교육/윤상혁멘토/프로젝트/UI/Re/test.csv', index=False, header=False)
            #except :
            #    pass
            
        
    ##########################################################################
        if treeclickvalue == 'UNALLOCATION':
            
        
            
            a = self.START_OFFSET.isChecked()
            b = self.END_OFFSET.isChecked()
            c = self.FILE_SIZE.isChecked()
            d = self.FOLDER.isChecked()
            e = self.FOLDER_INDEX.isChecked()
        
       
            r = [a,b,c,d,e]
        
            
            array = numpy.array(r)
            #print(array)
            wh = numpy.where(array == True)     
            index = wh[0]       #선택한 항목의 인덱스 값
            #print(index)
            print(len(index))
            
            
            df = []
            for i in result:
                for j in index:
                    df.append(i[j])
            
            dfslice = [df[i*len(index):(i+1)*len(index)] for i in range((len(df)-1+len(index))//len(index))]
            print(dfslice)
            
            column = columnlist[1:]
            #col = column
            #result.update({"h" : })
            
            #print(index)
            #d = OrderedDict(index)  #헤더 추가해서 csv에 보여지게
            #d.move_to_end('h',last=False)
            #print(d)
            
            df2 = pd.DataFrame(dfslice)
            
            col = []
            for i in index:
                col.append(column[i])
                
            print(col)
            
            
            df2.columns = col
            

            #print(df)
            #df2 = df.drop(index)

            #reverse = df2.transpose()
            #reverse = df2.transpose() # 행/열 바꾸기
            print(df2)
            
            
            ftypes = [('csv file','.csv')]
            ftitle = 'Save as..'
            savefile = filedialog.asksaveasfilename(filetypes=ftypes, title=ftitle)  #save file 경로 리턴
            #print(savefile+'.csv')
            
            df2.to_csv(savefile+'.csv', index=False)    #csv로 저장!

        
        
        if treeclickvalue == 'SLACK':
            
        
            
            a = self.FILE_NAME.isChecked()
            b = self.START_OFFSET.isChecked()
            c = self.END_OFFSET.isChecked()
            d = self.FILE_SIZE.isChecked()
            e = self.FOLDER.isChecked()
        
       
            r = [a,b,c,d,e]
        
            
            array = numpy.array(r)
            #print(array)
            wh = numpy.where(array == True)     
            index = wh[0]       #선택한 항목의 인덱스 값
            #print(index)
            print(len(index))
            
            
            df = []
            for i in result:
                for j in index:
                    df.append(i[j])
            
            dfslice = [df[i*len(index):(i+1)*len(index)] for i in range((len(df)-1+len(index))//len(index))]
            print(dfslice)
            
            column = columnlist[1:]
            #col = column
            #result.update({"h" : })
            
            #print(index)
            #d = OrderedDict(index)  #헤더 추가해서 csv에 보여지게
            #d.move_to_end('h',last=False)
            #print(d)
            
            df2 = pd.DataFrame(dfslice)
            
            col = []
            for i in index:
                col.append(column[i])
                
            print(col)
            
            
            df2.columns = col
            

            #print(df)
            #df2 = df.drop(index)

            #reverse = df2.transpose()
            #reverse = df2.transpose() # 행/열 바꾸기
            print(df2)
            
            
            ftypes = [('csv file','.csv')]
            ftitle = 'Save as..'
            savefile = filedialog.asksaveasfilename(filetypes=ftypes, title=ftitle)  #save file 경로 리턴
            #print(savefile+'.csv')
            
            df2.to_csv(savefile+'.csv', index=False)    #csv로 저장!
    
    
    
    def export_avi(self):
        #print(result)
        if treeclickvalue == 'ALLOCATION':
            try:
                aviargv = ' -e '
                for i in result:
                    aviargv += (i[6]+' ')
                
                print(aviargv)
                print(result)
                os.system('newcore.exe -p ' + path + aviargv)     #파일 추출은 folder_index로 추출 
                
                QMessageBox.information(widget,'Information','Complete exporting.' + ' \n[' + os.path.realpath('./') + '\\'+ result[0][5] + ']')

                #buttonReply = QMessageBox.question(widget, 'Load NxFS_Recovery', "Do you want to execute NxFS_Recovery program?", 
                #QMessageBox.Yes | QMessageBox.Cancel )
                #if buttonReply == QMessageBox.Yes:
                #    filepath = (os.popen('dir').readlines())[3]
                #    #print(filepath)
                #    pathforR = filepath.split()[0]
                
                #    print(pathforR)
                    #print(pathforR)
                    #폴더 지정시
                    #os.system('.\\dist\\recovery_main.exe '+ pathforR)
                    #print('.\\dist\\recovery_main.exe '+ pathforR +'\\' +result[0][6])
                    
                    #파일 지정시
                    #os.system('.\\dist\\recovery_main.exe '+ pathforR +'\\' +result[6])
            except :
                pass
            
        
        
        elif treeclickvalue == 'UNALLOCATION':
            try:
                aviargv = ' -u '
                for i in result:
                    aviargv += (i[4]+' ')
                
                print(result)
                    
                os.system('newcore.exe -p ' + path + aviargv)
                
                QMessageBox.information(widget,'Information','Complete exporting.' + ' \n[' + os.path.realpath('./') + '\\'+ result[0][3] + ']')

                #buttonReply = QMessageBox.question(widget, 'Load NxFS_Recovery', "Do you want to execute NxFS_Recovery program?", 
                #QMessageBox.Yes | QMessageBox.Cancel )
                #if buttonReply == QMessageBox.Yes:
                    #filepath = (os.popen('dir').readlines())[3]
                    #print(filepath)
                    #pathforR = filepath.split()[0]
                
                    #print(pathforR)
                    #폴더 지정시
                    #os.system('.\\dist\\recovery_main.exe '+ pathforR)
                    #print('.\\dist\\recovery_main.exe '+ pathforR +'\\' +result[0][1])
                    
                    #파일 지정시
                    #os.system('.\\dist\\recovery_main.exe '+ pathforR +'\\' +result[0][1])
            except:
                pass
        
        elif treeclickvalue == 'SLACK':
            try:
                aviargv = ' -s '
                for i in result:
                    aviargv += (i[0]+' ')
                    print(aviargv)
            
                print(result)
                    
                os.system('newcore.exe -p ' + path + aviargv)
                
                QMessageBox.information(widget,'Information','Complete exporting.' + ' \n[' + os.path.realpath('./') + '\\slack]')

                buttonReply = QMessageBox.question(widget, 'Load NxFS_Recovery', "Do you want to execute NxFS_Recovery program?", 
                QMessageBox.Yes | QMessageBox.Cancel )
                if buttonReply == QMessageBox.Yes:
                    filepath = (os.popen('dir').readlines())[3]
                    #print(filepath)
                    pathforR = filepath.split()[0]
                
                    #print(pathforR)
                    #폴더 지정시
                    os.system('recovery_main.exe '+ pathforR +'\\slack')
                    #print('.\\dist\\recovery_main.exe '+ pathforR +'\\slack')
                    
                    #파일 지정시
                    #os.system('.\\dist\\recovery_main.exe '+ pathforR +'\\' +result[0][0])
            except:
                pass
            
            #elif buttonReply == QMessageBox.Cancel:
            #    print("Cancel Clicked.")
            
            
            
if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    widget = QtWidgets.QWidget()

    ui = Ui_MainWindow()      #class로 정의한 UI Window
    ui.setupUi(MainWindow)
    
    MainWindow.setStyleSheet(
        "background-color : white;"
    )
    

        
    MainWindow.show()
    sys.exit(app.exec_())