from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QPushButton
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from GameParams import *
import numpy
import time
import xml.dom.minidom as xm
import Player
import Bot
import Bomb
import MyRect


class Game(QGraphicsView):

    end_signal = pyqtSignal(int)
    score_signal = pyqtSignal(int)

    def __init__(self):
        """
        Function creates MyView object.
        """
        QGraphicsView.__init__(self)
        self.__init_game()
        self.__init_ui()

    def __init_game(self):
        """
        Function initializes all backend game fields.
        :return:
        """
        self.bombs = []
        self.timer = QTimer()
        self.player = Player.Player(1, 1, 0)
        self.bots = [Bot.Bot(10 + (i + 1) * 6, 10 + (i + 1) * 6, i + 1) for i in range(num_of_bots)]
        self.score = 0
        self.create_board()
        self.move_dict = {
            Qt.Key_Left: self.move_left,
            Qt.Key_Right: self.move_right,
            Qt.Key_Up: self.move_up,
            Qt.Key_Down: self.move_down,
            Qt.Key_Space: self.add_bomb
        }
        for bot in self.bots:
            bot.remember_board(self.board)
            bot.remember_player_pos([self.player])
            bot.remember_bombs(self.bombs)

    def __init_ui(self):
        """
        Function initializes User Interface and Map view.
        :return:
        """
        self.scene = QGraphicsScene(0, 0, WINDOW_HEIGHT, WINDOW_WIDTH)
        self.view = QGraphicsView(self.scene)
        self.draw_board()
        self.setScene(self.scene)
        self.timer.timeout.connect(self.update)
        self.timer.start(10)
        self.timer_bots = QTimer()
        self.timer_bots.timeout.connect(self.move_bot)
        self.timer_bots.start(200)

        self.items = self.scene.items()

    def reinit_game(self):
        """
        Function gets game to init state.
        :return:
        """
        self.__init_game()
        self.__init_ui()

    def get_obj(self, x, y):
        """
        Function returns object in a map by coordinates.
        :param x: x coordinate of an object
        :param y: y coordiate of an object
        :return: Object.
        """
        for item in self.items:
            if item.x == x and item.y == y:
                return item
            else:
                return None

    def update(self):
        """
        Function handles all games parameters such as bombs boom,
        player death etc.
        Should be called periodically.

        :return:
        """
        for bomb in self.bombs:
            self.board[bomb.x][bomb.y] = 'XX'  # Add bomb to the board.
            self.draw_image(bomb.x, bomb.y, path_bomb)
        if self.player.alive:
            self.board[self.player.x][self.player.y] = 'OO'  # Add player to the board.
            self.draw_image(self.player.last_x, self.player.last_y, path_road)
            self.draw_image(self.player.x, self.player.y, path_bomberman)
        for bot in self.bots:
            if bot.alive:
                self.board[bot.x][bot.y] = 'BB'
                self.draw_image(bot.last_x, bot.last_y, path_road)
                self.draw_image(bot.x, bot.y, path_bot)

        self.score_signal.emit(self.score)
        self.boom()

    def read_board_xml(self, filename="map.xml"):
        """
        Function reads game map from the XML file.

        :param filename: Name of xml file.
        :return:
        """
        xmldoc = xm.parse(filename)
        rowslist = xmldoc.getElementsByTagName('row')

        for i in range(len(rowslist)):
            obj = rowslist[i].getElementsByTagName('obj')
            for j in range(len(obj)):
                self.board[i][j] = obj[j].firstChild.data

    def write_board_xml(self, filename="map.xml"):
        """
        Function writes game map to the XML file.

        :param filename: Name of xml file.
        :return:
        """
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

        with open(filename, 'w') as the_file:
            the_file.write(doc.toprettyxml())

    def draw_board(self):
        """
        Function draw whole game map.
        :return:
        """
        self.scene.clear()
        for bomba in self.bombs:
            self.board[bomba.X][bomba.Y] = 'XX'
        if self.player.alive:
            self.board[self.player.x][self.player.y] = 'OO'

        for bot in self.bots:
            if bot.alive:
                self.board[bot.x][bot.y] = 'BB'

        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == '##':
                    self.draw_image(i, j, path_cant_destroy)
                elif self.board[i][j] == '**':
                    self.draw_image(i, j, path_can_destroy)
                elif self.board[i][j] == '  ':
                    self.draw_image(i, j, path_road)
                elif self.board[i][j] == 'OO':
                    self.draw_image(i, j, path_bomberman)
                elif self.board[i][j] == 'XX':
                    self.draw_image(i, j, path_bomb)
                elif self.board[i][j] == 'BB':
                    self.draw_image(i, j, path_bot)

    def create_board(self):
        """
        Function creates game map.
        It's based on creating maze algorithm.
        :return:
        """
        temp = numpy.zeros((MAP_WIDTH, MAP_HEIGHT), dtype=bool)
        temp = temp.astype(str)
        for x in range(MAP_WIDTH):
            for y in range(MAP_HEIGHT):
                if x == 0 or y == 0 or x == MAP_WIDTH - 1 or y == MAP_HEIGHT - 1:
                    temp[x][y] = "##"
                elif x % 2 == 0 and y % 2 == 0:
                    temp[x][y] = "##"
                else:
                    temp[x][y] = "**"
                if temp[self.player.x + 1][self.player.y] != "##":
                    temp[self.player.x + 1][self.player.y] = "  "
                if temp[self.player.x][self.player.y + 1] != "##":
                    temp[self.player.x][self.player.y + 1] = "  "
                if temp[self.player.x + 2][self.player.y] != "##":
                    temp[self.player.x + 2][self.player.y] = "  "
                if temp[self.player.x][self.player.y + 2] != "##":
                    temp[self.player.x][self.player.y + 2] = "  "
                for i in range(len(self.bots)):
                    if temp[self.bots[i].x - 1][self.bots[i].y] != "##":
                        temp[self.bots[i].x - 1][self.bots[i].y] = "  "
                    if temp[self.bots[i].x][self.bots[i].y - 1] != "##":
                        temp[self.bots[i].x][self.bots[i].y - 1] = "  "
                    if temp[self.bots[i].x - 2][self.bots[i].y] != "##":
                        temp[self.bots[i].x - 2][self.bots[i].y] = "  "
                    if temp[self.bots[i].x][self.bots[i].y - 2] != "##":
                        temp[self.bots[i].x][self.bots[i].y - 2] = "  "

                temp[14][16] = "  "
                temp[16][14] = "  "
                temp[14][15] = "  "
                temp[15][17] = "  "
                temp[15][15] = "  "
                temp[15][14] = "  "

        self.board = temp

    def draw_image(self, x, y, path):
        """
        Function draw single image on game map.
        :param x: X coordinate of an image.
        :param y: Y coordinate of an image.
        :param path: path with an image to be printed.
        :return:
        """
        # Remove items from scene.
        self.items = self.scene.items()
        item = self.get_obj(x, y)
        if len(self.items) > MAP_HEIGHT * MAP_WIDTH:
            if item is not None:
                self.scene.removeItem(item)
        item = MyRect.MyRect(x, y, path)
        item.setAcceptHoverEvents(True)
        item.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        self.scene.addItem(item)

    def keyPressEvent(self, event):
        """
        Key press event.
        :param event:
        :return:
        """
        self.move_dict[event.key()](self.player)

    def move_up(self, player):
        """
        Function checks if player can go up. If can it moves, if can't it does nothing.

        :param player: Player to be moved.
        :return:
        """
        if player.y < MAP_HEIGHT - 1 and self.board[player.x][player.y + 1] != '**'\
                and self.board[player.x][player.y + 1] != '##':
            self.board[player.x][player.y] = '  '
            player.move('u')

    def move_down(self, player):
        """
        Function checks if player can go down. If can it moves, if can't it does nothing.

        :param player: Player to be moved.
        :return:
        """
        if player.y > 1 and self.board[player.x][player.y - 1] != '**'\
                and self.board[player.x][player.y - 1] != '##':
            self.board[player.x][player.y] = '  '
            player.move('d')

    def move_left(self, player):
        """
        Function checks if player can go left. If can it moves, if can't it does nothing.

        :param player: Player to be moved.
        :return:
        """
        if player.x > 1 and self.board[player.x - 1][player.y] != '**'\
                and self.board[player.x - 1][player.y] != '##':
            self.board[player.x][player.y] = '  '
            player.move('l')

    def move_right(self, player):
        """
        Function checks if player can go right. If can it moves, if can't it does nothing.

        :param player: Player to be moved.
        :return:
        """
        if player.x < MAP_HEIGHT - 1 and self.board[player.x + 1][player.y] != '**'\
                and self.board[player.x + 1][player.y] != '##':
            self.board[player.x][player.y] = '  '
            player.move('r')

    def add_bomb(self, player):
        """
        Function adds bomb to bombs list.

        :param player: Player which left the bomb.
        :return:
        """
        self.bombs.append(Bomb.Bomb(player.x , player.y , time.time() , player.ind))

    def boom(self):
        """
        Function handles bombs explosion.
        :return:
        """
        end = False
        for bomb in self.bombs:
            if time.time() - bomb.start > 3:
                self.clean_fields_after_boom(bomb)
                end = self.kill_players(bomb)
                self.bombs.remove(bomb)
                if bomb.owner == self.player.ind:
                    self.score += bomb_range
        if end:
            self.end_signal.emit(1)

    def clean_fields_after_boom(self, bomb):
        """
        Function cleans fields after bomb explosion.
        :param bomb:
        :return:
        """
        for field in bomb.get_cords_in_range():
            if 0 < field[0] < MAP_WIDTH and \
                0 < field[1] < MAP_HEIGHT and \
                self.board[field[0]][field[1]] != "##":
                self.board[field[0]][field[1]] = "  "
                self.draw_image(field[0], field[1], path_road)
        self.board[bomb.x][bomb.y] = "  "
        self.draw_image(bomb.x, bomb.y, path_road)

    def kill_players(self, bomb):
        """
        Function checks if player is killed by bomb.
        If is it returns True else returns False
        :param bomb: Bomb object
        :return:
        """
        for cords in bomb.get_cords_in_range():
            if (self.player.x, self.player.y) == cords:
                self.player.alive = False
            for bot in self.bots:
                if (bot.x, bot.y) == cords:
                    bot.alive = False

        return not self.player.alive

    def move_bot(self):
        """
        Function handles bot move.
        :return:
        """
        for bot in self.bots:
            old_x = bot.x
            old_y = bot.y
            bot.move()
            if bot.is_bomb_left():
                self.bombs.append(Bomb.Bomb(old_x, old_y, time.time(), 1))
                self.board[bot.last_x][bot.last_y] = "XX"
            else:
                self.board[old_x][old_y] = "  "
            self.board[bot.x][bot.y] = "BB"
            bot.remember_player_pos([self.player])
            bot.remember_board(self.board)
            bot.remember_bombs(self.bombs)
