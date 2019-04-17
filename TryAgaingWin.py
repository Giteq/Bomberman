from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import pyqtSignal
import sys
from QtTools import MyQMainWindow


class TryAgainWin(MyQMainWindow):

    try_again_sig = pyqtSignal(int)

    def __init__(self):
        super(TryAgainWin, self).__init__()
        self.msg = QMessageBox(QMessageBox.Question, "My title", "My text.", QMessageBox.Yes | QMessageBox.No)
        self.setCentralWidget(self.msg)
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setText("End of the game!!")
        self.msg.setInformativeText("Do You want to try again?")
        self.center_window_pos()
        self.show()

    def get_user_in(self):
        clicked = self.msg.exec_()

        if clicked == QMessageBox.Yes:
            self.try_again_sig.emit(1)
        elif clicked == QMessageBox.No:
            sys.exit()
