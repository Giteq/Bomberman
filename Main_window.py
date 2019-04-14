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
    def __init__(self):
        QGraphicsView.__init__(self)
        self.__init_game()
        self.__init_ui()

    def __init_game(self):
        self.MAP_HEIGHT = 24
        self.MAP_WIDTH = 24
        self.WINDOW_HEIGHT = 900
        self.WINDOW_WIDTH = 720
        self.RECT_HEIGHT = 28
        self.RECT_WIDTH = 28

        self.path_bomb = './Images/bomba.jpg'
        self.path_bomberman = './Images/Bombardman.jpg'
        self.path_bot = './Images/bot.png'
        self.path_can_destroy = './Images/do_rozwalenia.jfif'
        self.path_cant_destroy = './Images/nie_do_rozwalenia.jfif'
        self.path_road = './Images/droga.jpg'
        self.bombs = []
        self.num_of_bots = 1

        self.timer = QTimer()

        self.player = Player.Player(1, 1, 0)
        self.bots = [Bot.Bot(10 + (i + 1) * 6, 10 + (i + 1) * 6, i + 1) for i in range(self.num_of_bots)]
        self.score = 0
        self.create_board()
        for bot in self.bots:
            bot.remember_board(self.board)
            bot.remember_player_pos([self.player])
            bot.remember_bombs(self.bombs)

    def __init_ui(self):
        self.scene = QGraphicsScene(0, 0, self.WINDOW_HEIGHT, self.WINDOW_WIDTH)
        self.view = QGraphicsView(self.scene)
        self.draw_board()
        self.reset_button = QPushButton('Reset', self)
        self.reset_button.move(self.RECT_WIDTH * (self.MAP_HEIGHT + 1.5), self.RECT_WIDTH)
        self.reset_button.clicked.connect(self.clicked_reset)
        self.reset_button.setStyleSheet("background-color: red")
        self.reset_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.scene.addWidget(self.reset_button)
        self.setScene(self.scene)
        self.timer.timeout.connect(self.update)
        self.timer.start(10)
        self.timer_bots = QTimer()
        self.timer_bots.timeout.connect(self.move_bot)
        self.timer_bots.start(200)
        self.textbox = QtWidgets.QGraphicsTextItem()
        self.textbox.setPos(
            QtCore.QPointF(self.RECT_WIDTH * (self.MAP_HEIGHT + 1.5), self.RECT_WIDTH * 3))
        self.textbox.setPlainText("Score = " + str(self.score))

        self.scene.addItem(self.textbox)
        self.items = self.scene.items()

    def clicked_reset(self):
        self.__init_game()
        self.__init_ui()

    def initBoard(self):
        '''initiates board'''

        self.maz = self.maze(self.MAP_WIDTH , self.MAP_HEIGHT)
        self.create_board()
        for i in range(self.num_of_players):
            self.players.append(Player.Player(1, 1, i))

        self.curX = 0
        self.curY = 0
        self.numLinesRemoved = 0
        self.board = []

    def get_obj(self, x, y):
        for item in self.items:
            if item.x == x and item.y == y:
                return item
            else:
                return None

    def get_label_from_scene(self):
        ret = -1
        for i in range(len(self.items)):
            if isinstance(self.items[i], type(QtWidgets.QGraphicsTextItem())):
                ret = i
        return ret

    def update(self):
        self.textbox.setPlainText("Score = " + str(self.score))
        for bomb in self.bombs:
            self.board[bomb.X][bomb.Y] = 'XX'  # Add bomb to the board.
            self.draw_image(bomb.X, bomb.Y, self.path_bomb)
        if self.player.allive:
            self.board[self.player.X][self.player.Y] = 'OO'  # Add player to the board.
            self.draw_image(self.player.last_x, self.player.last_y, self.path_road)
            self.draw_image(self.player.X, self.player.Y, self.path_bomberman)
        for bot in self.bots:
            if bot.allive:
                self.board[bot.X][bot.Y] = 'BB'
                self.draw_image(bot.last_x, bot.last_y, self.path_road)
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

    def draw_board(self):
        self.scene.clear()
        for bomba in self.bombs:
            self.board[bomba.X][bomba.Y] = 'XX'
        if self.player.allive:
            self.board[self.player.X][self.player.Y] = 'OO'

        for bot in self.bots:
            if bot.allive:
                self.board[bot.X][bot.Y] = 'BB'

        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == '##':
                    self.draw_image(i, j, self.path_cant_destroy)
                elif self.board[i][j] == '**':
                    self.draw_image(i, j, self.path_can_destroy)
                elif self.board[i][j] == '  ':
                    self.draw_image(i, j, self.path_road)
                elif self.board[i][j] == 'OO':
                    self.draw_image(i, j, self.path_bomberman)
                elif self.board[i][j] == 'XX':
                    self.draw_image(i, j, self.path_bomb)
                elif self.board[i][j] == 'BB':
                    self.draw_image(i, j, self.path_bot)

    def create_board(self):
        temp = numpy.zeros((self.MAP_WIDTH, self.MAP_HEIGHT), dtype=bool)
        temp = temp.astype(str)
        for x in range(self.MAP_WIDTH):
            for y in range(self.MAP_HEIGHT):
                if x == 0 or y == 0 or x == self.MAP_WIDTH - 1 or y == self.MAP_HEIGHT - 1:
                    temp[x][y] = "##"
                elif x % 2 == 0 and y % 2 == 0:
                    temp[x][y] = "##"
                else:
                    temp[x][y] = "**"
                if temp[self.player.X + 1][self.player.Y] != "##":
                    temp[self.player.X + 1][self.player.Y] = "  "
                if temp[self.player.X][self.player.Y + 1] != "##":
                    temp[self.player.X][self.player.Y + 1] = "  "
                if temp[self.player.X + 2][self.player.Y] != "##":
                    temp[self.player.X + 2][self.player.Y] = "  "
                if temp[self.player.X][self.player.Y + 2] != "##":
                    temp[self.player.X][self.player.Y + 2] = "  "
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
        # Remove items from scene.
        self.items = self.scene.items()
        item = self.get_obj(x, y)
        if len(self.items) > self.MAP_HEIGHT * self.MAP_WIDTH:
            if item is not None:
                self.scene.removeItem(item)
        item = MyRect.MyRect(x, y, path)
        item.setAcceptHoverEvents(True)
        # item.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        self.scene.addItem(item)

    def keyPressEvent(self, event):
        '''processes key press events'''

        key = event.key()
        if key == Qt.Key_Left:
            if self.player.allive:
                self.move_left(self.player)

        elif key == Qt.Key_Right:
            if self.player.allive:
                self.move_right(self.player)

        elif key == Qt.Key_Down:
            if self.player.allive:
                self.move_down(self.player)

        elif key == Qt.Key_Up:
            if self.player.allive:
                self.move_up(self.player)

        elif key == Qt.Key_Space:
            if self.player.allive:
                self.add_bomb(self.player)

    def move_up(self, player):
        if player.Y < self.MAP_HEIGHT - 1 and self.board[player.X][player.Y + 1] != '**'\
                and self.board[player.X][player.Y + 1] != '##':
            self.board[player.X][player.Y] = '  '
            player.move('u')

    def move_down(self, player):
        if player.Y > 1 and self.board[player.X][player.Y - 1] != '**'\
                and self.board[player.X][player.Y - 1] != '##':
            self.board[player.X][player.Y] = '  '
            player.move('d')

    def move_left(self, player):
        if player.X > 1 and self.board[player.X - 1][player.Y] != '**'\
                and self.board[player.X - 1][player.Y] != '##':
            self.board[player.X][player.Y] = '  '
            player.move('l')

    def move_right(self, player):
        if player.X < self.MAP_HEIGHT - 1 and self.board[player.X + 1][player.Y] != '**'\
                and self.board[player.X + 1][player.Y] != '##':
            self.board[player.X][player.Y] = '  '
            player.move('r')

    def add_bomb(self, gracz):  # poruszanie sie
        self.bombs.append(Bomba.Bomba(gracz.X, gracz.Y, time.time(), gracz.indeks))

    def boom(self):
        for bomb in self.bombs:
            if time.time() - bomb.start > 3:
                self.clean_fields_after_boom(bomb)
                self.kill_players(bomb)
                self.bombs.remove(bomb)
                if bomb.wlasciciel == self.player.indeks:
                    self.score += 1

    def clean_fields_after_boom(self, bomb):
        if self.board[bomb.X][bomb.Y + 1] != "##":
            self.board[bomb.X][bomb.Y + 1] = "  "
            self.draw_image(bomb.X, bomb.Y + 1, self.path_road)

        if self.board[bomb.X][bomb.Y - 1] != "##":
            self.board[bomb.X][bomb.Y - 1] = "  "
            self.draw_image(bomb.X, bomb.Y - 1, self.path_road)

        if self.board[bomb.X + 1][bomb.Y] != "##":
            self.board[bomb.X + 1][bomb.Y] = "  "
            self.draw_image(bomb.X + 1, bomb.Y, self.path_road)

        if self.board[bomb.X - 1][bomb.Y] != "##":
            self.board[bomb.X - 1][bomb.Y] = "  "
            self.draw_image(bomb.X - 1, bomb.Y, self.path_road)

        self.board[bomb.X][bomb.Y] = "  "
        self.draw_image(bomb.X, bomb.Y, self.path_road)

    def kill_players(self, bomb):
        if self.player.X == bomb.X + 1 and self.player.Y == bomb.Y:
            self.player.allive = False
        if self.player.X == bomb.X - 1 and self.player.Y == bomb.Y:
            self.player.allive = False
        if self.player.X == bomb.X and self.player.Y == bomb.Y + 1:
            self.player.allive = False
        if self.player.X == bomb.X and self.player.Y == bomb.Y - 1:
            self.player.allive = False
        for bot in self.bots:
            if bot.X == bomb.X + 1 and bot.Y == bomb.Y:
                bot.allive = False
            if bot.X == bomb.X - 1 and bot.Y == bomb.Y:
                bot.allive = False
            if bot.X == bomb.X and bot.Y == bomb.Y + 1:
                bot.allive = False
            if bot.X == bomb.X and bot.Y == bomb.Y - 1:
                bot.allive = False

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
            bot.remember_player_pos([self.player])
            bot.remember_board(self.board)
            bot.remember_bombs(self.bombs)


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.view = MyView()
        self.setCentralWidget(self.view)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    view = Window()
    view.show()
    sys.exit(app.exec_())

