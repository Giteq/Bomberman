from PyQt5 import QtWidgets
from Game import Game
from TryAgaingWin import TryAgainWin
import sys


class WindowsManager(QtWidgets.QMainWindow):
    def __init__(self):
        super(WindowsManager, self).__init__()
        self.view = Game()
        self.view.end_signal.connect(self.end)
        self.setCentralWidget(self.view)
        self.try_again = None

    def end(self, value):
        if value == 1:
            self.try_again = TryAgainWin()
            self.try_again.try_again_sig.connect(self.try_again_handle)
            self.try_again.get_user_in()

    def try_again_handle(self, value):
        if value == 1:
            self.try_again.close()
            self.view.clicked_reset()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    view = WindowsManager()
    view.show()
    sys.exit(app.exec_())

