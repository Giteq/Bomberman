from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from GameMap import MyView
import sys


class TryAgain(QtWidgets.QMainWindow):
    def __init__(self):
        super(TryAgain, self).__init__()
        msg = QMessageBox(QMessageBox.Question, "My title", "My text.", QMessageBox.Yes | QMessageBox.No)
        self.setCentralWidget(msg)
        msg.setIcon(QMessageBox.Information)
        msg.setText("End of the game!!")
        msg.setInformativeText("Do You want to try again?")
        self.show()
        clicked = msg.exec_()

        if clicked == QMessageBox.Yes:
            print("Yes")


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.view = MyView()
        self.view.end_signal.connect(self.end)
        self.setCentralWidget(self.view)
        self.try_again = None

    def end(self, value):
        if value == 1:
            self.try_again = TryAgain()
            self.try_again.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    view = Window()
    view.show()
    sys.exit(app.exec_())

