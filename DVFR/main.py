from View.Analysis_main import Analysis_main


class MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(950, 650)

        self.Analysis_main = Analysis_main(MainWindow)

if __name__ == "__main__":
    from PyQt5 import QtWidgets
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Window = QtWidgets.QMainWindow()
    ui = MainWindow()
    ui.setupUi(Window)
    Window.show()
    sys.exit(app.exec_())
