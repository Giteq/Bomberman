from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QVBoxLayout , QWidget , QPushButton , QLabel , QGridLayout
from qtpy import QtCore

from Game import Game
from TryAgaingWin import TryAgainWin
import sys
from QtTools import MyQMainWindow


class MainWindow(MyQMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        grid_layout = QGridLayout()

        main_layout = QVBoxLayout()
        self.score_label = QLabel()
        self.score_label.setText("Score: 0")
        grid_layout.addWidget(self.score_label, 0, 0)

        # Game
        self.game = Game()
        self.view = QWidget()
        main_layout.addWidget(self.game)
        # Button
        self.reset_button = QPushButton('Reset', self)
        self.reset_button.clicked.connect(self.reset_clicked)
        self.reset_button.setStyleSheet("background-color: red")
        self.reset_button.setFocusPolicy(QtCore.Qt.NoFocus)
        grid_layout.addWidget(self.reset_button, 0, 1)

        main_layout.addLayout(grid_layout)
        self.game.end_signal.connect(self.end)
        self.game.score_signal.connect(self.change_score)
        self.view.setLayout(main_layout)
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

    def change_score(self, score):
        self.score_label.setText(f"Score: {score}")

    def reset_clicked(self):
        self.game.reinit_game()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    view = MainWindow()
    view.show()
    sys.exit(app.exec_())

