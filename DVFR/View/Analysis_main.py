from importlib.util import MAGIC_NUMBER
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QAction, QFileDialog
from PyQt5.QtGui import QIcon, QPixmap
import os


class Analysis_main():
    def __init__(self, MainWindow):
        self.load_item = QtWidgets.QTextEdit() # 불러온 영상 리스트 보여줌
        self.fileInfo_item = QtWidgets.QListWidgetItem() # File Info
        self.Result_item = QtWidgets.QListWidgetItem()   # Result

        self.ui_frame(MainWindow)   # ui 뼈대??

        self.active_main(MainWindow)

    def active_main(self, MainWindow):
        self.menubar(MainWindow)    # menubar
        
        # --------------------- 불러온 영상 리스트 ---------------------
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(10, 10, 281, 541))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents_4 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_4.setGeometry(QtCore.QRect(0, 0, 279, 539))
        self.scrollAreaWidgetContents_4.setObjectName("scrollAreaWidgetContents_4")
        self.listWidget = QtWidgets.QListWidget(self.scrollAreaWidgetContents_4)
        self.listWidget.setGeometry(QtCore.QRect(0, 0, 281, 541))
        self.listWidget.setObjectName("listWidget")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_4)

        # --------------------- Tab widget ---------------------
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(300, 10, 621, 541))
        self.tabWidget.setObjectName("tabWidget")

        # --------------------- File Info ---------------------
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.scrollArea_2 = QtWidgets.QScrollArea(self.tab)
        self.scrollArea_2.setGeometry(QtCore.QRect(0, 0, 621, 521))
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 619, 519))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.textBrowser = QtWidgets.QTextBrowser(self.scrollAreaWidgetContents)
        self.textBrowser.setGeometry(QtCore.QRect(0, 0, 621, 521))
        self.textBrowser.setObjectName("textBrowser")
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents)
        self.tabWidget.addTab(self.tab, "")

        # --------------------- Result ---------------------
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.scrollArea_3 = QtWidgets.QScrollArea(self.tab_2)
        self.scrollArea_3.setGeometry(QtCore.QRect(0, 0, 621, 521))
        self.scrollArea_3.setWidgetResizable(True)
        self.scrollArea_3.setObjectName("scrollArea_3")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 619, 519))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")

        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_2)
        self.scrollArea_3.setWidget(self.scrollAreaWidgetContents_2)


        self.tabWidget.addTab(self.tab_2, "")

        # ---------------------------------

        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Damaged Video File Retore (DVFR)"))
        self.pushButton_2.setText(_translate("MainWindow", "삭제"))
        self.pushButton.setText(_translate("MainWindow", "추출"))
        
        # --------------------- File Info ---------------------
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), "File Info")
        self.listWidget.itemSelectionChanged.connect(self.File_info)

        # --------------------- Result ---------------------
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), "Result")
        self.listWidget.itemSelectionChanged.connect(self.show_Result)  # 눌린 listwidjet에 따라서.

        # --------------------- delete ---------------------
        self.pushButton_2.clicked.connect(self.file_del)

        # --------------------- menu bar ---------------------
        self.menufile.setTitle(_translate("MainWindow", "file"))
        self.menusetting.setTitle(_translate("MainWindow", "setting"))
        self.menuabout.setTitle(_translate("MainWindow", "about"))
        self.actionopen.setText(_translate("MainWindow", "open"))
        self.actionabout_us.setText(_translate("MainWindow", "about us"))

        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def File_info(self):
        # 파일 정보 (추가 예정)
        item = self.listWidget.currentItem()
        if item:
            file_size = os.path.getsize(item.text())
            self.textBrowser.setHtml("file name: " + QtCore.QFileInfo(item.text()).fileName() + "<br>" + "file path: " + item.text()
            + "<br>" + "Size: " + str(file_size) + " bytes" + "<br>" + "전체 영상: " + "" + "<br>" + "손상된 영상: " + "")
        else:
            self.textBrowser.setHtml("")

    def ui_frame(self, MainWindow):
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 550, 281, 51))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_2 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(300, 550, 621, 51))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.progressBar = QtWidgets.QProgressBar(self.horizontalLayoutWidget_2)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout_2.addWidget(self.progressBar)

    def menubar(self, MainWindow):
        # --------------------- menu bar ---------------------
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 954, 26))
        self.menubar.setObjectName("menubar")
        
        # menu list
        self.menu_file(MainWindow)
        self.menu_setting(MainWindow)
        self.menu_about(MainWindow)

        # menubar
        MainWindow.setMenuBar(self.menubar)
        
        # status bar
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # menu bar action
        self.menubar.addAction(self.menufile.menuAction())
        self.menubar.addAction(self.menusetting.menuAction())
        self.menubar.addAction(self.menuabout.menuAction())

    def menu_file(self, MainWindow):
        # file menu
        self.menufile = QtWidgets.QMenu(self.menubar)
        self.menufile.setObjectName("menufile")

        # open file
        self.file_open(MainWindow)

    def file_open(self, MainWindow):
        # -------- File open --------
        self.actionopen = QtWidgets.QAction(MainWindow)
        self.actionopen.setObjectName("actionopen")
        openFile = QAction(QIcon('open.png'), 'Open', self.menufile)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open New File')
        openFile.triggered.connect(self.showDialog)
        
        self.menufile.addAction(openFile)

    def showDialog(self):   
        # 불러온 영상 리스트
        file_loc = QFileDialog.getOpenFileName(self.menufile, 'Open file', './')
        self.load_item.setText(file_loc[0])  # 
        query = self.load_item.toPlainText()
        self.listWidget.addItem(query)

    def menu_setting(self, MainWindow): # setting menu
        self.menusetting = QtWidgets.QMenu(self.menubar)
        self.menusetting.setObjectName("menusetting")
    
    def menu_about(self, MainWindow):   # about menu
        self.menuabout = QtWidgets.QMenu(self.menubar)
        self.menuabout.setObjectName("menuabout")

        # about us
        self.actionabout_us = QtWidgets.QAction(MainWindow)
        self.actionabout_us.setObjectName("actionabout_us")
        self.menuabout.addAction(self.actionabout_us)

    def file_del(self):
        rn = self.listWidget.currentRow()
        self.listWidget.takeItem(rn)

    def dialog_open(self, file_path):  # open이 안되는 현상 발생.
        self.dialog = QtWidgets.QDialog()
        file = self.sender().objectName()

        # 이미지 출력
        photo = QtWidgets.QLabel(self.dialog)
        photo.setPixmap(QPixmap(file_path + file))
        photo.setContentsMargins(10,10,10,10)
        photo.resize(photo.width()+400, photo.height()+400)
        photo.setScaledContents(True)
        photo.setObjectName("photo")

        #QDialog 세팅
        self.dialog.setWindowTitle(file)
        self.dialog.resize(500,450)
        self.dialog.show()

    def show_Result(self):
        x = 0
        y = 0
        # signature = {'jpeg_head':bytes([0xFF, 0xD8, 0xFF, 0xE0, 0x00, 0x10, 0x4A, 0x46, 0x49, 0x46])}
        # file_path = self.listWidget.currentItem().text()
        file_path = "View/image/"

        
        for file in os.listdir(file_path):
            if(x == 4):
                x = 0
                y += 1

            # 버튼 안의 아이콘으로 이미지 출력
            self.button_img = QtWidgets.QPushButton()
            self.button_img.setIcon(QIcon(file_path + file))
            self.button_img.setIconSize(QtCore.QSize(100,100))
            self.button_img.setObjectName(file)
            #self.button_img.setText(file)
            #self.button_img.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            #self.button_img.setStyleSheet('PushButton{background-color:rgba(0,0,0,0)')
            #self.button_img.setStyleSheet('PushButton{border-color:rgba(0,0,0,0)')
            # self.button_img.clicked.connect(self.dialog_open(file_path))  # 이미지 크게 보기
            
            self.gridLayout.addWidget(self.button_img, y, x)
            x += 1