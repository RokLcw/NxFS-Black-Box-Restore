from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(954, 653)
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
        for i in range(0, 10):
            item = QtWidgets.QListWidgetItem()
            self.listWidget.addItem(item)
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
        self.listWidget_2 = QtWidgets.QListWidget(self.scrollAreaWidgetContents)
        self.listWidget_2.setGeometry(QtCore.QRect(0, 0, 621, 521))
        self.listWidget_2.setObjectName("listWidget_2")
        for i in range(0, 10):
            item = QtWidgets.QListWidgetItem()
            self.listWidget_2.addItem(item)
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
        self.listWidget_3 = QtWidgets.QListWidget(self.scrollAreaWidgetContents_2)
        self.listWidget_3.setGeometry(QtCore.QRect(0, 0, 621, 521))
        self.listWidget_3.setObjectName("listWidget_3")
        for i in range(0, 10):
            item = QtWidgets.QListWidgetItem()
            self.listWidget_3.addItem(item)
        self.scrollArea_3.setWidget(self.scrollAreaWidgetContents_2)
        self.tabWidget.addTab(self.tab_2, "")
        
        # --------------------- Under ---------------------
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 954, 26))
        self.menubar.setObjectName("menubar")
        self.menufile = QtWidgets.QMenu(self.menubar)
        self.menufile.setObjectName("menufile")
        self.menusetting = QtWidgets.QMenu(self.menubar)
        self.menusetting.setObjectName("menusetting")
        self.menuabout = QtWidgets.QMenu(self.menubar)
        self.menuabout.setObjectName("menuabout")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionopen = QtWidgets.QAction(MainWindow)
        self.actionopen.setObjectName("actionopen")
        
        # --------------------- status bar ---------------------
        self.menufile.addAction(self.actionopen)
        self.menubar.addAction(self.menufile.menuAction())
        self.menubar.addAction(self.menusetting.menuAction())
        self.menubar.addAction(self.menuabout.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_2.setText(_translate("MainWindow", "삭제"))
        self.pushButton.setText(_translate("MainWindow", "추출"))

        # --------------------- 불러온 영상 리스트 ---------------------
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        for i in range(0, 10):
            item = self.listWidget.item(i)
            item.setText(_translate("MainWindow", "새 항목"))
        self.listWidget.setSortingEnabled(__sortingEnabled)

        # --------------------- File Info ---------------------
        __sortingEnabled = self.listWidget_2.isSortingEnabled()
        self.listWidget_2.setSortingEnabled(False)
        for i in range(0, 10):
            item = self.listWidget_2.item(i)
            item.setText(_translate("MainWindow", "새 항목"))
        self.listWidget_2.setSortingEnabled(__sortingEnabled)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "File Info"))
        __sortingEnabled = self.listWidget_3.isSortingEnabled()

        # --------------------- Result ---------------------
        self.listWidget_3.setSortingEnabled(False)
        for i in range(0, 10):
            item = self.listWidget_3.item(i)
            item.setText(_translate("MainWindow", "새 항목"))
        self.listWidget_3.setSortingEnabled(__sortingEnabled)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Result"))

        # --------------------- status bar ---------------------
        self.menufile.setTitle(_translate("MainWindow", "file"))
        self.menusetting.setTitle(_translate("MainWindow", "setting"))
        self.menuabout.setTitle(_translate("MainWindow", "about"))
        self.actionopen.setText(_translate("MainWindow", "open"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
