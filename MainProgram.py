import sys
import PyQt5
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from program.ChessMain import ChessMainClass
from design.menugame1 import Ui_MainWindow
from design.menugame2 import Ui_MainWindowPlay

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class MainWindow:
    def __init__(self):
        self.main_win = QMainWindow()
        self.uic = Ui_MainWindow()
        self.uicplay = Ui_MainWindowPlay()
        self.uic.setupUi(self.main_win)
        self.uic.btn_NewGame.clicked.connect(self.showgame)
    
    def show(self):
        self.main_win.show()
    
    def showgame(self):
        self.uicplay.setupUi(self.main_win)
        self.uicplay.btn_OnePlay.clicked.connect(self.onePlay)
        self.uicplay.btn_TwoPlay.clicked.connect(self.twoPlay)
        # self.main_win.hide()
        # self.mainkkk = ChessMainClass(False, True)
        # sys.exit(app.exec())
    def onePlay(self):
        self.main_win.hide()
        self.mainkkk = ChessMainClass(True, False)
        sys.exit(app.exec())
    def twoPlay(self):
        self.main_win.hide()
        self.mainkkk = ChessMainClass(True, True)
        sys.exit(app.exec())
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())