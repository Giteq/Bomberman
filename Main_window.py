from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QPushButton
from PyQt5.QtCore import Qt, QTimer
import sys
import numpy
import time
import xml.dom.minidom as xm
import Player
import Bot
import Bomba
import MyRect

class MyView(QGraphicsView):
    WYSOKOSC_MAPY = 24
    SZEROKOSC_MAPY = 24

    WYSOKOSC_OKNA = 900
    SZEROKOSC_OKNA = 720

    WYSOKOSC_KWADRATU = 28
    SZEROKOSC_KWADRATU = 28

    path_bomb = './Images/bomba.jpg'
    path_bomberman = './Images/Bombardman.jpg'
    path_bot = './Images/bot.png'
    path_can_destroy = './Images/do_rozwalenia.jfif'
    path_cant_destroy = './Images/nie_do_rozwalenia.jfif'
    path_road = './Images/droga.jpg'
    players = []
    bots = []
    bombs = []
    ind_actual_player = 0
    num_of_players = 1
    num_of_bots = 1

    timer = QTimer()

    def __init__(self):
        QGraphicsView.__init__(self)
        self.scene = QGraphicsScene(0, 0, self.WYSOKOSC_OKNA, self.SZEROKOSC_OKNA)
        for i in range(self.num_of_players):
            self.players.append(Player.Player(1 + i * 10, 1 + i * 10, i))

        for i in range(self.num_of_bots):
            self.bots.append(Bot.Bot(10 + (i + 1) * 6, 10 + (i + 1) * 6, i + 1))

        self.score = 0
        self.view = QGraphicsView(self.scene)
        self.create_board()
        for bot in self.bots:
            bot.remember_board(self.board)
            bot.remember_player_pos(self.players)
            bot.remember_bombs(self.bombs)
        self.draw_board()
        #Guzik
        self.reset_button = QPushButton('Reset', self)
        self.reset_button.move(self.SZEROKOSC_KWADRATU*(self.WYSOKOSC_MAPY + 1.5), self.SZEROKOSC_KWADRATU)
        self.reset_button.clicked.connect(self.clicked_reset)
        self.reset_button.setStyleSheet("background-color: red")
        self.reset_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.scene.addWidget(self.reset_button)
        self.setScene(self.scene)
        self.timer.timeout.connect(self.update)
        self.timer.start(10)
        self.timer_boty = QTimer()
        self.timer_boty.timeout.connect(self.move_bot)
        self.timer_boty.start(200)
        self.textbox = QtWidgets.QGraphicsTextItem()
        self.textbox.setPos(
            QtCore.QPointF(self.SZEROKOSC_KWADRATU * (self.WYSOKOSC_MAPY + 1.5), self.SZEROKOSC_KWADRATU * 3))
        self.textbox.setPlainText("Score = " + str(self.score))

        self.scene.addItem(self.textbox)

    def clicked_reset(self):
        self.create_board()
        for gracz in self.players:
            gracz.reset()
        for i in range(self.num_of_players):
            self.players.append(Player.Player(1 + i * 10, 1 + i * 10, i))
        for i in range(self.num_of_bots):
            self.bots.append(Bot.Bot(10 + (i + 1) * 6, 10 + (i + 1) * 6, i))

        self.bombs.clear()
        self.draw_board()


    def initBoard(self):
        '''initiates board'''

        self.maz = self.maze(self.SZEROKOSC_MAPY, self.WYSOKOSC_MAPY)
        self.create_board()
        for i in range(self.num_of_players):
            self.players.append(Player.Player(1, 1, i))

        self.curX = 0
        self.curY = 0
        self.numLinesRemoved = 0
        self.board = []

    def get_obj_ind(self, x, y):
        for i in range(len(self.itemy)):
            if self.itemy[i].x == x and self.itemy[i].y == y:
                return i

    def get_label_from_scene(self):
        ret = -1
        for i in range(len(self.itemy)):
            if type(self.itemy[i]) == type(QtWidgets.QGraphicsTextItem()):
                ret = i
        return ret

    def update(self):
        self.textbox.setPlainText("Score = " + str(self.score))

        for bomba in self.bombs:
            self.board[bomba.X][bomba.Y] = 'XX'  # wstawiamy bomby w plansze
            self.draw_image(bomba.X, bomba.Y, self.path_bomb)
        for gracz in self.players:
            if gracz.zywy:
                self.board[gracz.X][gracz.Y] = 'OO'  # wstawiamy gracza w plansze (usuwanie starego pionka gracza w linijce 57)
                self.draw_image(gracz.wczesniejsze_x, gracz.wczesniejsze_y, self.path_road)
                self.draw_image(gracz.X, gracz.Y, self.path_bomberman)

        for bot in self.bots:
            if bot.zywy:
                self.board[bot.X][bot.Y] = 'BB'
                self.draw_image(bot.wczesniejsze_x, bot.wczesniejsze_y, self.path_road)
                self.draw_image(bot.X, bot.Y, self.path_bot)

        self.boom()

    def read_board_xml(self):
        xmldoc = xm.parse('somefile.xml')

        rowslist = xmldoc.getElementsByTagName('row')

        for i in range(len(rowslist)):
            obj = rowslist[i].getElementsByTagName('obj')
            for j in range(len(obj)):
                self.board[i][j] = obj[j].firstChild.data
        print(self.board)


    def write_board_xml(self):
        doc = xm.Document()
        map_elem = doc.createElement("mapa")
        for i in range(len(self.board)):
            row_elem = doc.createElement("row")

            for j in range(len(self.board[0])):
                obj_elem = doc.createElement("obj")
                row_elem.appendChild(obj_elem)
                obj_elem.appendChild(doc.createTextNode(self.board[i][j]))
            map_elem.appendChild(row_elem)
        doc.appendChild(map_elem)
        # doc.writexml(sys.stdout)
        #print(doc.toprettyxml())

        with open('somefile.xml', 'w') as the_file:
            the_file.write(doc.toprettyxml())

    def draw_board(self):  # rysowanie planszy
        self.scene.clear()
        for bomba in self.bombs:
            self.board[bomba.X][bomba.Y] = 'XX'  # wstawiamy bomby w plansze
        for gracz in self.players:
            if gracz.zywy:
                self.board[gracz.X][gracz.Y] = 'OO'  # wstawiamy gracza w plansze (usuwanie starego pionka gracza w linijce 57)

        for bot in self.bots:
            if bot.zywy:
                self.board[bot.X][bot.Y] = 'BB'

        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == '##':
                    self.draw_image(i, (j), self.path_cant_destroy)
                elif self.board[i][j] == '**':
                    self.draw_image(i, (j), self.path_can_destroy)
                elif self.board[i][j] == '  ':
                    self.draw_image(i, (j), self.path_road)

                elif self.board[i][j] == 'OO':
                    path = self.path_bomberman
                    self.draw_image( i,  + (j), path)

                elif self.board[i][j] == 'XX':
                    path = self.path_bomb
                    self.draw_image(i, (j, path))

                elif self.board[i][j] == 'BB':
                    path = self.path_bot
                    self.draw_image(i, (j), path)

    def create_board(self):  # tworzenie planszy stringow z tablicy true/false wygenerowanej przez funkcje maze
        temp = numpy.zeros((self.SZEROKOSC_MAPY, self.WYSOKOSC_MAPY), dtype=bool)
        temp = temp.astype(str)
        for x in range(self.SZEROKOSC_MAPY):
            for y in range(self.WYSOKOSC_MAPY):
                if x == 0 or y == 0 or x == self.SZEROKOSC_MAPY - 1 or y == self.WYSOKOSC_MAPY - 1:
                    temp[x][y] = "##"
                elif x%2 == 0 and y%2 == 0:
                    temp[x][y] = "##"
                else:
                    temp[x][y] = "**"
                for i in range(len(self.players)):
                    if temp[self.players[i].X + 1][self.players[i].Y] != "##":
                        temp[self.players[i].X + 1][self.players[i].Y] = "  "
                    if temp[self.players[i].X][self.players[i].Y + 1] != "##":
                        temp[self.players[i].X][self.players[i].Y + 1] = "  "
                    if temp[self.players[i].X + 2][self.players[i].Y] != "##":
                        temp[self.players[i].X + 2][self.players[i].Y] = "  "
                    if temp[self.players[i].X][self.players[i].Y + 2] != "##":
                        temp[self.players[i].X][self.players[i].Y + 2] = "  "
                for i in range(len(self.bots)):
                    if temp[self.bots[i].X - 1][self.bots[i].Y] != "##":
                        temp[self.bots[i].X - 1][self.bots[i].Y] = "  "
                    if temp[self.bots[i].X][self.bots[i].Y - 1] != "##":
                        temp[self.bots[i].X][self.bots[i].Y - 1] = "  "
                    if temp[self.bots[i].X - 2][self.bots[i].Y] != "##":
                        temp[self.bots[i].X - 2][self.bots[i].Y] = "  "
                    if temp[self.bots[i].X][self.bots[i].Y - 2] != "##":
                        temp[self.bots[i].X][self.bots[i].Y - 2] = "  "

                temp[14][16] = "  "
                temp[16][14] = "  "
                temp[14][15] = "  "
                temp[15][17] = "  "
                temp[15][15] = "  "
                temp[15][14] = "  "
        self.board = temp

    def draw_image(self, x, y, path):
        #Usuwanie itemow ze sceny
        self.itemy = self.scene.items()
        if len(self.itemy) > self.WYSOKOSC_MAPY * self.SZEROKOSC_MAPY:
            ind = self.get_obj_ind(x, y)
            self.scene.removeItem(self.itemy[ind])
        self.item = MyRect.MyRect(x, y, path)
        self.item.setAcceptHoverEvents(True)
        self.item.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        self.scene.addItem(self.item)

    def keyPressEvent(self, event):
        '''processes key press events'''

        key = event.key()

        if key == Qt.Key_P:
            self.pause()
            return

        elif key == Qt.Key_Left:
            if self.players:
                self.move_left(self.players[self.ind_actual_player])

        elif key == Qt.Key_Right:
            if self.players:
                self.move_right(self.players[self.ind_actual_player])

        elif key == Qt.Key_Down:
            if self.players:
                self.move_down(self.players[self.ind_actual_player])

        elif key == Qt.Key_Up:
            if self.players:
                self.move_up(self.players[self.ind_actual_player])

        elif key == Qt.Key_Space:
            if self.players:
                if self.players[self.ind_actual_player].zywy:
                    self.add_bomb(self.players[self.ind_actual_player])

        elif key == Qt.Key_D:
            self.oneLineDown()

    def move_up(self, gracz):
        if gracz.Y < self.WYSOKOSC_MAPY - 1 and self.board[gracz.X][gracz.Y + 1] != '**' and self.board[gracz.X][gracz.Y + 1] != '##':
            self.board[gracz.X][gracz.Y] = '  '  # zastapienie starej pozycji gracza pustym polem
            gracz.wczesniejsze_x = gracz.X
            gracz.wczesniejsze_y = gracz.Y
            gracz.Y += 1

    def move_down(self, gracz):
        if gracz.Y > 1 and self.board[gracz.X][gracz.Y - 1] != '**' and self.board[gracz.X][gracz.Y - 1] != '##':
            self.board[gracz.X][gracz.Y] = '  '  # zastapienie starej pozycji gracza pustym polem
            gracz.wczesniejsze_x = gracz.X
            gracz.wczesniejsze_y = gracz.Y
            gracz.Y -= 1

    def move_left(self, gracz):
        if gracz.X > 1 and self.board[gracz.X - 1][gracz.Y] != '**' and self.board[gracz.X - 1][gracz.Y] != '##':
            self.board[gracz.X][gracz.Y] = '  '  # zastapienie starej pozycji gracza pustym polem
            gracz.wczesniejsze_x = gracz.X
            gracz.wczesniejsze_y = gracz.Y
            gracz.X -= 1

    def move_right(self, gracz):
        if gracz.X < self.WYSOKOSC_MAPY - 1 and self.board[gracz.X + 1][gracz.Y] != '**' and self.board[gracz.X + 1][gracz.Y] != '##':
            self.board[gracz.X][gracz.Y] = '  '  # zastapienie starej pozycji gracza pustym polem
            gracz.wczesniejsze_x = gracz.X
            gracz.wczesniejsze_y = gracz.Y
            gracz.X += 1

    def add_bomb(self, gracz):  # poruszanie sie
        self.bombs.append(Bomba.Bomba(gracz.X, gracz.Y, time.time(), gracz.indeks))
        # do listy bomb dodajemy w ktorej turze została postawiona i jej koordynaty

    #Obsluga wybuchania bomba
    def boom(self):
        for bomba in self.bombs:
            if time.time() - bomba.start > 3:
            #if bomba.wybuchnieta:
                self.clean_fields_after_boom(bomba)
                self.kill_players(bomba)
                self.bombs.remove(bomba)
                if bomba.wlasciciel == self.players[self.ind_actual_player].indeks:
                    self.score += 1

    #Czyszczenie pol naokolo bomby
    def clean_fields_after_boom(self, bomba):
        if self.board[bomba.X][bomba.Y + 1] != "##":
            self.board[bomba.X][bomba.Y + 1] = "  "
            self.draw_image(bomba.X, bomba.Y + 1, self.path_road)

        if self.board[bomba.X][bomba.Y - 1] != "##":
            self.board[bomba.X][bomba.Y - 1] = "  "
            self.draw_image(bomba.X, bomba.Y - 1, self.path_road)

        if self.board[bomba.X + 1][bomba.Y] != "##":
            self.board[bomba.X + 1][bomba.Y] = "  "
            self.draw_image(bomba.X + 1, bomba.Y, self.path_road)

        if self.board[bomba.X - 1][bomba.Y] != "##":
            self.board[bomba.X - 1][bomba.Y] = "  "
            self.draw_image(bomba.X - 1, bomba.Y, self.path_road)

        self.board[bomba.X][bomba.Y] = "  "
        self.draw_image(bomba.X, bomba.Y, self.path_road)

    def kill_players(self, bomba):
        for gracz in self.players:
            if gracz.X == bomba.X + 1 and gracz.Y == bomba.Y:
                gracz.zywy = False
            if gracz.X == bomba.X - 1 and gracz.Y == bomba.Y:
                gracz.zywy = False
            if gracz.X == bomba.X and gracz.Y == bomba.Y + 1:
                gracz.zywy = False
            if gracz.X == bomba.X and gracz.Y == bomba.Y - 1:
                gracz.zywy = False
        for bot in self.bots:
            if bot.X == bomba.X + 1 and bot.Y == bomba.Y:
                bot.zywy = False
            if bot.X == bomba.X - 1 and bot.Y == bomba.Y:
                bot.zywy = False
            if bot.X == bomba.X and bot.Y == bomba.Y + 1:
                bot.zywy = False
            if bot.X == bomba.X and bot.Y == bomba.Y - 1:
                bot.zywy = False

    def move_bot(self):
        for bot in self.bots:
            stare_x = bot.X
            stare_y = bot.Y
            bot.move()
            if bot.is_bomb_left():
                self.bombs.append(Bomba.Bomba(stare_x, stare_y, time.time(), 1))
                self.board[stare_x][stare_y] = "XX"
            else:
                self.board[stare_x][stare_y] = "  "
            self.board[bot.X][bot.Y] = "BB"
            bot.remember_player_pos(self.players)
            bot.remember_board(self.board)
            bot.remember_bombs(self.bombs)

class window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(window, self).__init__()
        self.view = MyView()
        self.setCentralWidget(self.view)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    view = window()
    view.show()
    sys.exit(app.exec_())

