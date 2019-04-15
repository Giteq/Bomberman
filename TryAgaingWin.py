from PyQt5.QtWidgets import QMessageBox, QMainWindow
from PyQt5.QtCore import pyqtSignal
import sys


class TryAgainWin(QMainWindow):

    try_again_sig = pyqtSignal(int)

    def __init__(self):
        super(TryAgainWin, self).__init__()
        self.msg = QMessageBox(QMessageBox.Question, "My title", "My text.", QMessageBox.Yes | QMessageBox.No)
        self.setCentralWidget(self.msg)
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setText("End of the game!!")
        self.msg.setInformativeText("Do You want to try again?")
        self.show()

    def get_user_in(self):
        clicked = self.msg.exec_()

        if clicked == QMessageBox.Yes:
            self.try_again_sig.emit(1)
        elif clicked == QMessageBox.No:
            sys.exit()