from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QImage
from GameParams import *


class MyRect(QtWidgets.QGraphicsRectItem):
    def __init__(self, x, y, path):
        super().__init__(RECT_WIDTH + x * RECT_WIDTH,\
                                                RECT_HEIGHT + (MAP_WIDTH - y - 1) *\
                                                RECT_HEIGHT, RECT_HEIGHT, RECT_HEIGHT)
        self.x = x
        self.y = y

        image = QImage(path)
        image = image.scaled(RECT_HEIGHT, RECT_WIDTH, Qt.IgnoreAspectRatio)
        brush = QBrush(image)
        self.setBrush(brush)

        # self.color = color
        # col = QLinearGradient()
        # col.setColorAt(0.1, self.color)
        # self.setBrush(col)

    def mouseReleaseEvent(self, event):
        # Do your stuff here.
        print('Jestem sobie tutaj: ', end='')
        print(self.x, end='')
        print(", ", end="")
        print(self.y)
        return QtWidgets.QGraphicsRectItem.mouseReleaseEvent(self, event)

    # def hoverMoveEvent(self, event):
    #     # Do your stuff here.
    #     pass
