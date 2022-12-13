from asyncio import sleep
from datetime import datetime
from View.media_frame_extraction import frame_ext as frameEx
from View.image_process import image_process
from View.slack_frame_extraction import slack_ext
from View.avi_extraction import avi_ext

import csv, time, glob
import itertools
import os, threading, pyautogui 
from functools import partial
from pathlib import Path

import pandas as pd
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
import os
from functools import partial
import itertools
from pathlib import Path

from .PlayVideo import VideoPlayer

class Analysis_main():

    def __init__(self, MainWindow):

        self.load_item = QtWidgets.QTextEdit() # 불러온 영상 리스트 보여줌
        self.fileInfo_item = QtWidgets.QListWidgetItem() # File Info
        self.Result_item = QtWidgets.QListWidgetItem()   # Result
        self.offset_item = QtWidgets.QListWidgetItem()   # Offset

        self.ui_frame(MainWindow)   # ui 뼈대??

        self.active_main(MainWindow)

    def active_main(self, MainWindow):

        self.menubar(MainWindow)    # menubar
        
        # 변환 파일 저장할 디렉터지 선택
        self.folder = QtWidgets.QFileDialog.getExistingDirectory(None, '변환된 파일이 저장될 위치를 선택하세요.')

        # --------------------- 불러온 영상 리스트 ---------------------
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(10, 10, 281, 541))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 279, 539))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.listWidget = QtWidgets.QListWidget(self.scrollAreaWidgetContents)
        self.listWidget.setGeometry(QtCore.QRect(0, 0, 281, 541))
        self.listWidget.setObjectName("listWidget")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)


        # 마우스 우클릭 메뉴

        self.listWidget.setContextMenuPolicy(Qt.ActionsContextMenu)
        action = QtWidgets.QAction("영상 저장", self.listWidget)
        action.installEventFilter(self.listWidget)
        action.triggered.connect(self.mouseRightClickEvent)

        self.listWidget.addAction(action)

        # --------------------- Tab widget ---------------------
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(300, 10, 621, 541))
        self.tabWidget.setObjectName("tabWidget")

        # --------------------- File Info ---------------------
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.scrollArea_1 = QtWidgets.QScrollArea(self.tab)
        self.scrollArea_1.setGeometry(QtCore.QRect(0, 0, 621, 521))
        self.scrollArea_1.setWidgetResizable(True)
        self.scrollArea_1.setObjectName("scrollArea_1")
        self.scrollAreaWidgetContents_1 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_1.setGeometry(QtCore.QRect(0, 0, 619, 519))
        self.scrollAreaWidgetContents_1.setObjectName("scrollAreaWidgetContents_1")
        self.textBrowser = QtWidgets.QTextBrowser(self.scrollAreaWidgetContents_1)
        self.textBrowser.setGeometry(QtCore.QRect(0, 0, 621, 521))
        self.textBrowser.setObjectName("textBrowser")
        self.scrollArea_1.setWidget(self.scrollAreaWidgetContents_1)
        self.tabWidget.addTab(self.tab, "")

        # --------------------- Result ---------------------
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.scrollArea_2 = QtWidgets.QScrollArea(self.tab_2)
        self.scrollArea_2.setGeometry(QtCore.QRect(0, 0, 621, 521))
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 619, 519))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")

        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_2)
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)


        self.tabWidget.addTab(self.tab_2, "")

        #--------------------- Offset_1 ---------------------
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.scrollArea_3 = QtWidgets.QScrollArea(self.tab_3)
        self.scrollArea_3.setGeometry(QtCore.QRect(0, 0, 621, 521))
        self.scrollArea_3.setWidgetResizable(True)
        self.scrollArea_3.setObjectName("scrollArea_3")
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 619, 519))
        self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
        
        self.tableWidget = QtWidgets.QTableWidget(self.scrollAreaWidgetContents_3)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, 619, 519))
        self.tableWidget.setObjectName("tableWidget")
        self.scrollArea_3.setWidget(self.scrollAreaWidgetContents_3)

        self.tabWidget.addTab(self.tab_3, "")

        #--------------------- Offset_2 ---------------------
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.scrollArea_4 = QtWidgets.QScrollArea(self.tab_4)
        self.scrollArea_4.setGeometry(QtCore.QRect(0, 0, 621, 521))
        self.scrollArea_4.setWidgetResizable(True)
        self.scrollArea_4.setObjectName("scrollArea_4")
        self.scrollAreaWidgetContents_4 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_4.setGeometry(QtCore.QRect(0, 0, 619, 519))
        self.scrollAreaWidgetContents_4.setObjectName("scrollAreaWidgetContents_4")
        
        self.tableWidget_2 = QtWidgets.QTableWidget(self.scrollAreaWidgetContents_4)
        self.tableWidget_2.setGeometry(QtCore.QRect(0, 0, 619, 519))
        self.tableWidget_2.setObjectName("tableWidget")
        self.scrollArea_4.setWidget(self.scrollAreaWidgetContents_4)

        self.tabWidget.addTab(self.tab_4, "")
        
        # ---------------------------------

        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Damaged Video File Retore (DVFR)"))
        self.pushButton_2.setText(_translate("MainWindow", "삭제"))
        self.pushButton.setText(_translate("MainWindow", "변환"))
        
        # --------------------- File Info ---------------------
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), "File Info")
        self.listWidget.itemSelectionChanged.connect(self.File_info) # 눌린 listwidjet에 따라서

        # --------------------- Result ---------------------

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), "Result")
        self.listWidget.itemSelectionChanged.connect(self.show_Result)

        # --------------------- Offset_1 ---------------------
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), "Offset_전방")
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(["id", "Ch.", "Offset", "EndOffset", "Size", "Damaged", "Etc"]) 
        self.tableWidget.setAlternatingRowColors(True) # 행 색깔 다르게
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers) # 리스트 내용 변경 금지
        self.tableWidget.setSortingEnabled(True) # 정렬
        self.listWidget.itemSelectionChanged.connect(self.show_offset_1)

        # --------------------- Offset_2 ---------------------
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), "Offset_후방")
        self.tableWidget_2.setColumnCount(7)
        self.tableWidget_2.setHorizontalHeaderLabels(["id", "Ch.", "Offset", "EndOffset", "Size", "Damaged", "Etc"]) 
        self.tableWidget_2.setAlternatingRowColors(True) # 행 색깔 다르게
        self.tableWidget_2.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers) # 리스트 내용 변경 금지
        self.tableWidget_2.setSortingEnabled(True) # 정렬
        self.listWidget.itemSelectionChanged.connect(self.show_offset_2)

        # --------------------- delete ---------------------
        self.pushButton_2.clicked.connect(self.file_del)

        # --------------------- transform ---------------------
        self.pushButton.clicked.connect(self.file_trf)

        # --------------------- menu bar ---------------------
        self.menufile.setTitle(_translate("MainWindow", "file"))
        self.menusetting.setTitle(_translate("MainWindow", "setting"))
        self.menuabout.setTitle(_translate("MainWindow", "about"))

        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def File_info(self):
        # 파일 정보 (추가 예정)
        item = self.listWidget.currentItem()
        if item:
            file_size = os.path.getsize(item.text())
            #self.textBrowser.setHtml("file name: " + QtCore.QFileInfo(item.text()).fileName() + "<br>" + "file path: " + item.text()
            #+ "<br>" + "Size: " + str(file_size) + " bytes" + "<br>" + "전체 영상: " + "" + "<br>" + "손상된 영상: " + "")
            self.textBrowser.setHtml("file name: " + QtCore.QFileInfo(item.text()).fileName() + "<br>" + "file path: " + item.text()
            + "<br>" + "Size: " + str(file_size) + " bytes")
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
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(650, 550, 261, 51))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2") # progressBar
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(300, 550, 241, 51))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3") # lineEdit
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        # --------------------- progress bar ---------------------
        self.progressBar = QtWidgets.QProgressBar(self.horizontalLayoutWidget_2)
        self.progressBar.setGeometry(QtCore.QRect(650, 560, 261, 31))
        self.timer = QtCore.QBasicTimer()
        #self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setAlignment(Qt.AlignRight)
        self.progressBar.setValue(0)
        self.progressBar.setFormat('')
        # setting background color
        self.progressBar.setStyleSheet("QProgressBar"
                          "{"
                          "background-color : transparent;"
                          "border : 1px"
                          "}")
        #self.progressBar.hide()
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

        # -------- File open --------
        self.actionopen = QtWidgets.QAction(MainWindow)
        self.actionopen.setObjectName("actionopen")
        openFile = QtWidgets.QAction(QIcon('open.png'), 'Open_File', self.menufile)
        openFile.setShortcut('Ctrl+I')
        openFile.setStatusTip('Open New File')
        openFile.triggered.connect(self.showDialog_file)

        '''
        openFolder = QtWidgets.QAction( 'Open_Folder', self.menufile)
        openFolder.setShortcut('Ctrl+O')
        openFolder.setStatusTip('Open New Folder')
        openFolder.triggered.connect(self.showDialog_folder)
        '''

        openSlack = QtWidgets.QAction( 'Open_Slack_File', self.menufile)
        openSlack.setShortcut('Ctrl+S')
        openSlack.setStatusTip('Open Slack File')
        openSlack.triggered.connect(self.showDialog_folder)
        
        self.menufile.addAction(openFile)
        #self.menufile.addAction(openFolder)
        self.menufile.addAction(openSlack)

    def menu_setting(self, MainWindow): # setting menu
        self.menusetting = QtWidgets.QMenu(self.menubar)
        self.menusetting.setObjectName("menusetting")

        # find
        self.actionFind = QtWidgets.QAction(MainWindow)
        self.actionFind.setObjectName("actionFind")
        find = QtWidgets.QAction('Find', self.actionFind)
        find.setShortcut("Ctrl+F")
        find.setStatusTip('find offset')
        find.triggered.connect(self.show_search)

        self.menusetting.addAction(find)
        
    
    def menu_about(self, MainWindow):   # about menu
        self.menuabout = QtWidgets.QMenu(self.menubar)
        self.menuabout.setObjectName("menuabout")

        # about us
        self.actionabout_us = QtWidgets.QAction(MainWindow)
        self.actionabout_us.setObjectName("actionabout_us")
        about = QtWidgets.QAction('about_us', self.actionabout_us)

        self.menuabout.addAction(about)

    def file_del(self):
        rn = self.listWidget.currentRow()
        self.listWidget.takeItem(rn)

    # 검색창 보이기
    def show_search(self):
        self.lineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget_3)
        self.lineEdit.setGeometry(QtCore.QRect(1, 13, 239, 24))
        self.lineEdit.setObjectName("lineEdit")

        self.horizontalLayout_3.addWidget(self.lineEdit)

        self.lineEdit.setPlaceholderText("Search...")
        self.lineEdit.textChanged.connect(self.search)

    # 검색 기능
    def search(self):
        word = self.lineEdit.text().lower()

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

    # 불러온 영상 파일 리스트
    def showDialog_file(self):   
        file_loc = QtWidgets.QFileDialog.getOpenFileName(self.menufile, 'Open file', './', 'avi(*.avi)')
        #file_loc = QtWidgets.QFileDialog.getOpenFileName(self.menufile, 'Open file', './')
        if file_loc[0]:
            self.load_item.setText(file_loc[0]) 
            query = self.load_item.toPlainText()
            self.listWidget.addItem(query)
        else:
            pass


    # 불러온 영상 폴더 리스트
    def showDialog_folder(self):   
        file_loc = QtWidgets.QFileDialog.getExistingDirectory(self.menufile, 'Open folder', './')
        if file_loc:
            self.load_item.setText(file_loc) 
            query = self.load_item.toPlainText()
            self.listWidget.addItem(query)

        else:
            pass

    # 마우스 우클릭 시 영상 저장 
    def mouseRightClickEvent(self):
        #self.progressBar.setFormat('영상 저장 중')
        
        item = self.listWidget.currentItem()
        input_data = QtCore.QFileInfo(item.text()).filePath()
        input_name = QtCore.QFileInfo(item.text()).fileName()

        full_folder = (f"{self.folder}/result/{input_name}/result")
        print(full_folder)

        self.avi_ext = avi_ext(self, full_folder, input_data)
        #self.avi_end.connect(self.frame_end)


    # '변환' 버튼 클릭 시 수행 함수
    def file_trf(self):

        self.progressBar.setFormat('로딩 중입니다...')

        if self.folder:
            item = self.listWidget.currentItem()
            input_data = QtCore.QFileInfo(item.text()).filePath()
            input_name = QtCore.QFileInfo(item.text()).fileName()

            #data =  self.input_data
            full_folder = (f"{self.folder}/result/{input_name}")

            global path
            path = (f"{self.folder}/result/{input_name}/result")
            #path = "C:/Users/vkdrk/OneDrive/바탕화~1-LAPTOP-FBS87IKO-51235/result/20221204_011228"

            # avi 파일 선택 시 실행
            if('.avi' in input_data):
                self.frame_ex = frameEx(full_folder, input_data)
                self.frame_ex.start()
                self.frame_ex.create_file.connect(partial(self.signal_1, input_data))
                self.frame_ex.frame_end.connect(self.frame_end)
            else:
                self.slack_ex = slack_ext(full_folder, input_data)
                self.slack_ex.start()
                self.slack_ex.avi_end.connect(self.avi_end)
                        
        else:
            pass


    # 이미지 클릭 시 확대
    def dialog_open(self, file): 
        self.windows = []

        #print(file)

        ext = file.split('.')

        '''
        if(ext[1] == 'mp4'):            
            videoplayer = VideoPlayer(file)
            self.windows.append(videoplayer)
            videoplayer.resize(640, 480)
            videoplayer.setWindowTitle(file)
            videoplayer.show()
                        
        else:
        '''

        self.dialog = QtWidgets.QDialog()

        # 이미지 출력
        photo = QtWidgets.QLabel(self.dialog)
        photo.setPixmap(QPixmap(file))
        photo.setContentsMargins(10,10,10,10)
        photo.resize(photo.width()+400, photo.height()+400)
        photo.setScaledContents(True)
        photo.setObjectName("photo")

        #QDialog 세팅
        self.dialog.setWindowTitle(file)
        self.dialog.resize(500,450)
        self.dialog.show()

    # Result 탭에 이미지 보여주기
    def show_Result(self): 
        #global folName
        #folName = "20221130_204449"
        #apath = "C:/Users/vkdrk/OneDrive/바탕화~1-LAPTOP-FBS87IKO-51235/result/20221204_011228"

        #Layout의 모든 widget 메소드 삭제
        for i in range(self.gridLayout.count()):
            self.gridLayout.itemAt(i).widget().deleteLater() 

        item = self.listWidget.currentItem()
        input_name = QtCore.QFileInfo(item.text()).fileName()
        input_data = QtCore.QFileInfo(item.text()).filePath()

        if(os.path.isdir(f"{self.folder}/result/{input_name}/")):

            if('.avi' in input_data):
                #path = (f"{self.folder}/result/{input_name}/result/{save_folder_name}")
                path = (f"{self.folder}/result/{input_name}/result")

                image_path = path + '/frame_image_front/'

                x = 0
                y = 0
                
                for i in range(2):
                    if(i == 0):
                        self.label = QtWidgets.QLabel()
                        self.label.setGeometry(QtCore.QRect(0, 0, 650, 521))
                        #self.label.setText("전방 프레임")
                        self.gridLayout.addWidget(self.label)
                        x=4

                    if(i == 1):
                        x=0
                        y += 1
                        image_path = path + '/frame_image_back/'
                        self.label = QtWidgets.QLabel()
                        self.label.setGeometry(QtCore.QRect(0, 0, 650, 521))
                        #self.label.setText("후방 프레임")
                        self.gridLayout.addWidget(self.label)
                        x=4
                        y+=1
                        
                    for file in os.listdir(image_path):
                        
                        if(x == 4):
                            x = 0
                            y += 1

                        # 버튼 안의 아이콘으로 이미지 출력
                        self.button_img = QtWidgets.QPushButton()
                        
                        ext = file.split('.')
                        if(ext[1] == 'mp4'):
                            self.button_img.setIcon(QIcon("play_button.png"))
                        else:
                            self.button_img.setIcon(QIcon(image_path + file))

                        self.button_img.setIconSize(QtCore.QSize(140,80))
                        self.button_img.clicked.connect(partial(self.dialog_open, file = image_path+file))  # 이미지 크게 보기
                        
                        self.gridLayout.addWidget(self.button_img, y, x)
                        x += 1
                    
                self.progressBar.setFormat('이미지 로드 완료')
            
            else:
                # slack 이미지 나열
                path = (f"{self.folder}/result/{input_name}/result")
                img_path = path + '/frame/'
                x = 0
                y = 0
                print(img_path)
                for file in os.listdir(img_path):
                    if('.jpg' in file):
                        if(x == 4):
                            x = 0
                            y += 1

                        # 버튼 안의 아이콘으로 이미지 출력
                        self.button_img = QtWidgets.QPushButton()

                        self.button_img.setIcon(QIcon(img_path + file))
                        self.button_img.setIconSize(QtCore.QSize(140,80))
                        self.button_img.clicked.connect(partial(self.dialog_open, file = img_path+file))  # 이미지 크게 보기
                        self.gridLayout.addWidget(self.button_img, y, x)
                        x += 1

                self.progressBar.setFormat('완료')

        else:
            pass

    
    # verticalHeader 클릭하면 진수 변경
    def transhex_1(self):
        print("진수 변경")
        if('0x' in str(self.tableWidget.item(0,2).text())):
            #print(self.tableWidget.rowCount())
            for i in range(self.tableWidget.rowCount()):
                for j in range(3):
                    dec = int(self.tableWidget.item(i,j+2).text(), 16)
                    self.tableWidget.setItem(i, j+2, QtWidgets.QTableWidgetItem(str(dec)))
        else:
            for i in range(self.tableWidget.rowCount()):
                for j in range(3):
                    hexa = hex(int(self.tableWidget.item(i,j+2).text()))
                    self.tableWidget.setItem(i, j+2, QtWidgets.QTableWidgetItem(str(hexa)))

    def transhex_2(self):
        print("진수 변경")
        if('0x' in str(self.tableWidget_2.item(0,2).text())):
            #print(self.tableWidget.rowCount())
            for i in range(self.tableWidget_2.rowCount()):
                for j in range(3):
                    dec = int(self.tableWidget_2.item(i,j+2).text(), 16)
                    self.tableWidget_2.setItem(i, j+2, QtWidgets.QTableWidgetItem(str(dec)))
        else:
            for i in range(self.tableWidget_2.rowCount()):
                for j in range(3):
                    hexa = hex(int(self.tableWidget_2.item(i,j+2).text()))
                    self.tableWidget_2.setItem(i, j+2, QtWidgets.QTableWidgetItem(str(hexa)))


    # item 창 클릭하면 진수 변경
    def transhex_pframe(self):
        cnt = self.treeWidget_click.topLevelItemCount()
        if('0x' in self.treeWidget_click.topLevelItem(1).text(2)):
            for i in range(cnt):
                temp_item = self.treeWidget_click.topLevelItem(i)
                for j in range(3):
                    dec = int(temp_item.text(j+1), 16)
                    temp_item.setText(j+1, str(dec))
        else:
            for i in range(cnt):
                temp_item = self.treeWidget_click.topLevelItem(i)
                for j in range(3):
                    hexa = hex(int(temp_item.text(j+1), 16))
                    temp_item.setText(j+1, str(hexa))

    # offset 정보 나열 
    def show_offset_1(self):
        # 테이블의 모든 행 삭제
        self.tableWidget.setRowCount(0)

        item = self.listWidget.currentItem()
        input_name = QtCore.QFileInfo(item.text()).fileName()
                
        if(os.path.isdir(f"{self.folder}/result/{input_name}/")):

            #path = "C:/Users/vkdrk/OneDrive/바탕화~1-LAPTOP-FBS87IKO-51235/result/20221204_011228"
            path = (f"{self.folder}/result/{input_name}/result")

            with open(path+'/offset_info.csv', 'rt') as f:
                #x=0
                reader = csv.reader(f)
                next(reader, None)  # skip the headers
                for row in reader:
                    if(row[2] == '00') or (row[2] == 'unknown'):
                        if(row[2] == '00'):
                            self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), "Offset_전방")
                        else:
                            self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), "Offset")
                        rowPosition = self.tableWidget.rowCount()  #현재 table 행 개수 return
                        self.tableWidget.insertRow(rowPosition)
                        for i in range(5):
                            if(i<2):
                                self.tableWidget.setItem(rowPosition, i, QtWidgets.QTableWidgetItem(row[i+1]))
                            elif(i<5):
                                self.tableWidget.setItem(rowPosition, i, QtWidgets.QTableWidgetItem(str(hex(int(row[i+1], 16)))))

            self.tableWidget.itemClicked.connect(partial(self.onItemClicked, path))
            self.tableWidget.verticalHeader().sectionClicked.connect(self.transhex_1)

        else:
            pass

    # offset 정보 나열 
    def show_offset_2(self):
        # 테이블의 모든 행 삭제
        self.tableWidget_2.setRowCount(0)

        item = self.listWidget.currentItem()
        input_name = QtCore.QFileInfo(item.text()).fileName()
                
        if(os.path.isdir(f"{self.folder}/result/{input_name}/")):

            #path = "C:/Users/vkdrk/OneDrive/바탕화~1-LAPTOP-FBS87IKO-51235/result/20221204_011228"
            path = (f"{self.folder}/result/{input_name}/result")

            with open(path+'/offset_info.csv', 'rt') as f:
                reader = csv.reader(f)
                next(reader, None)  # skip the headers
                for row in reader:
                    if(row[2] == '01'):
                        self.tabWidget.setTabVisible(3, True)
                        rowPosition = self.tableWidget_2.rowCount()  #현재 table 행 개수 return
                        self.tableWidget_2.insertRow(rowPosition)
                        for i in range(5):
                            if(i<2):
                                self.tableWidget_2.setItem(rowPosition, i, QtWidgets.QTableWidgetItem(row[i+1]))
                            elif(i<5):
                                self.tableWidget_2.setItem(rowPosition, i, QtWidgets.QTableWidgetItem(str(hex(int(row[i+1], 16)))))
                    else:
                        self.tabWidget.setTabVisible(3, False)

            self.tableWidget_2.itemClicked.connect(partial(self.onItemClicked, path))
            self.tableWidget_2.verticalHeader().sectionClicked.connect(self.transhex_2)

        else:
            pass

    #@QtCore.pyqtSlot(QtWidgets.QTableWidgetItem, int)
    def onItemClicked(self, path):
        #apath = "C:/Users/vkdrk/OneDrive/바탕화~1-LAPTOP-FBS87IKO-51235/result/20221204_011228"

        row = self.tableWidget.currentIndex().row()
        print(row)

        # 'offset_info_pframe' 파일 있는지 확인
        if os.path.isfile(path + "/offset_info_pframe.csv"):
            file = pd.read_csv(path + "/offset_info.csv")

            idx = file.iloc[row, 1]
            ch = file.iloc[row, 2]

            self.windows = []
            
            self.dialog_pframe = QtWidgets.QDialog()
            self.treeWidget_click = QtWidgets.QTreeWidget(self.dialog_pframe)
            self.treeWidget_click.setGeometry(QtCore.QRect(0, 0, 619, 519))
            self.treeWidget_click.setObjectName("treeWidget_click")
            self.treeWidget_click.setColumnCount(5)
            #self.tableWidget_click.setHorizontalHeaderLabels(["Ch." , "Offset" , "EndOffset", "Size", "Damaged"]) 
            self.treeWidget_click.setHeaderLabels(["Ch." , "Offset" , "EndOffset", "Size", "Damaged"])
            self.treeWidget_click.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers) # 리스트 내용 변경 금지
            self.treeWidget_click.setAlternatingRowColors(True)

            with open(path + '/offset_info_pframe.csv', 'rt') as f:
                x=0
                reader = csv.reader(f)
                next(reader, None)  # skip the headers
                for row in reader:
                    if(int(row[1]) == idx):
                        if(int(row[2]) == ch):
                            QtWidgets.QTreeWidgetItem(self.treeWidget_click, row[2:]) 
                    x += 1

            self.treeWidget_click.setSortingEnabled(True)
            #self.head = self.treeWidget_click.header()
            self.treeWidget_click.itemClicked.connect(self.transhex_pframe)

            #QDialog 세팅
            self.dialog_pframe.setWindowTitle("Detail")
            self.dialog_pframe.resize(500,450)
            self.dialog_pframe.show()

        else:
            pass

    # frame offset 파일 저장 완료 후 실행
    def signal_1(self, input_data):
        self.image_proc = image_process(input_data, path)
        self.image_proc.start()
        self.show_offset_1()
        self.show_offset_2()

        self.image_proc.create_image.connect(partial(self.show_Result))

    def signal_slack(self):
        self.show_offset_1()
        self.show_Result()

    # frame offset 파일 저장 완료 후 progressBar 상태메시지 변경
    def frame_end(self):
        self.progressBar.setFormat('offset 값 저장 완료. 이미지 로드 중')

    def avi_end(self):
        self.progressBar.setFormat('영상 저장')

'''
# 영상 출력 클래스
class VideoPlayer(QMainWindow):
    
    def __init__(self, file):
        path = "View/image(fake)/result/" + str(input_data) + "/"

        super().__init__()

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        videoWidget = QVideoWidget()

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(QApplication.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.error = QLabel()
        self.error.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        # 파일 경로 설정
        fileName = path + file
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
        self.playButton.setEnabled(True)

        # 창 위젯 생성
        wid = QWidget(self)
        self.setCentralWidget(wid)
    
        # 레이아웃 생성
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)
 
        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addLayout(controlLayout)
        layout.addWidget(self.error)

        # Set widget to contain window contents
        wid.setLayout(layout)
    
        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)

        self.playButton.setEnabled(True)

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()
 
    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    QtWidgets.QApplication.style().standardIcon(QtWidgets.QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    QtWidgets.QApplication.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay))
 
    def positionChanged(self, position):
        self.positionSlider.setValue(position)
 
    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)
 
    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)
 
    def handleError(self):
        self.playButton.setEnabled(False)
        self.error.setText("Error: " + self.mediaPlayer.errorString())
'''