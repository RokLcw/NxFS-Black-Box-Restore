from View.Analysis_main import Analysis_main
from PyQt5.QtGui import QIcon

class MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(950, 650)
        #MainWindow.setWindowIcon(QIcon('main_logo.ico'))
        MainWindow.setWindowIcon(QIcon('../main_logo.ico'))
    
        self.Analysis_main = Analysis_main(MainWindow)

if __name__ == "__main__":
    from PyQt5 import QtWidgets, QtCore
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Window = QtWidgets.QMainWindow()
    ui = MainWindow()
    ui.setupUi(Window)
    Window.show()
    sys.exit(app.exec_())
