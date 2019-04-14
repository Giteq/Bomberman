from GameParams import *
from Player import Player


class Bot(Player):
    def __init__(self, x, y, ind):
        super().__init__(x, y, ind)
        self.left_bomb = False
        self.players = []
        self.board = []
        self.bombs = []

    def reset(self):
        self.x = 1
        self.y = 1
        self.alive = True

    def remember_board(self, board):
        self.board = board

    def remember_player_pos(self, players):
        self.players = players

    def remember_bombs(self, bombs):
        self.bombs = bombs

    def is_bomb_there(self, direction):
        if direction == "r":
            if self.x + 2 < MAP_WIDTH and self.y + 1 < MAP_WIDTH and self.x > 0 and self.y > 0:
                if self.board[self.x+1][self.y+1] == "XX" or self.board[self.x+2][self.y] == "XX" or self.board[self.x+1][self.y-1] == "XX" or \
                        self.board[self.x+1][self.y] == "XX" or self.board[self.x+1][self.y] == "##" or self.board[self.x][self.y] == "XX":
                    return True
        if direction == "l":
            if self.x - 2 < MAP_WIDTH and self.y + 1 < MAP_WIDTH and self.x > 0 and self.y > 0:
                if self.board[self.x-1][self.y+1] == "XX" or self.board[self.x-2][self.y] == "XX" or self.board[self.x-1][self.y-1] == "XX" or \
                        self.board[self.x - 1][self.y] == "XX" or self.board[self.x-1][self.y] == "##" or self.board[self.x][self.y] == "XX":
                    return True
        if direction == "u":
            if self.y - 2 < MAP_WIDTH and self.x + 1 < MAP_WIDTH and self.x > 0 and self.y > 0:
                if self.board[self.x][self.y-2] == "XX" or self.board[self.x+1][self.y-1] == "XX" or self.board[self.x-1][self.y-1] == "XX" or \
                        self.board[self.x][self.y - 1] == "XX" or self.board[self.x][self.y-1] == "##" or self.board[self.x][self.y] == "XX":
                    return True
        if direction == "d":
            if self.y + 2 < MAP_WIDTH and self.x + 1 < MAP_WIDTH and self.x > 0 and self.y > 0:
                if self.board[self.x+1][self.y+1] == "XX" or self.board[self.x][self.y+2] == "XX" or self.board[self.x-1][self.y+1] == "XX" or \
                        self.board[self.x][self.y+1] == "XX" or self.board[self.x][self.y+1] == "##" or self.board[self.x][self.y] == "XX":
                    return True

        return False

    def where_is_player(self):
        ret_val = []
        if self.players[0].x < self.x:
            ret_val.append("l")
            ret_val.append("r")
        if self.players[0].x > self.x:
            ret_val.append("r")
            ret_val.append("l")
        if self.players[0].y > self.y:
            ret_val.append("d")
            ret_val.append("u")
        if self.players[0].y < self.y:
            ret_val.append("u")
            ret_val.append("d")
        if self.players[0].x == self.x:
            ret_val.append("e")
            if self.players[0].y > self.y:
                ret_val.append("u")
            if self.players[0].y < self.y:
                ret_val.append("d")
        if self.players[0].y == self.y:
            if self.players[0].x > self.x:
                ret_val.append("r")
            if self.players[0].x < self.x:
                ret_val.append("l")
            ret_val.append("e")

        return ret_val

    def is_obstacle_there(self, dir):
        if dir == "r":
            if self.board[self.x + 1][self.y] == "**":
                return True
        if dir == "l":
            if self.board[self.x - 1][self.y] == "**":
                return True
        if dir == "u":
            if self.board[self.x][self.y - 1] == "**":
                return True
        if dir == "d":
            if self.board[self.x][self.y + 1] == "**":
                return True
        return False

    def leave_bomb(self):
        self.left_bomb = True

    def is_bomb_left(self):
        return self.left_bomb

    def change_cords(self, move, move2):
        if move == "r":
            self.x +=1
        if move  == "l":
            self.x -= 1
        if move == "u":
            self.y -= 1
        if move == "d":
            self.y += 1
        if move == "e":
            if move2 == "l":
                self.y -= 1
            if move2 == "r":
                self.y += 1
        if move2 == "e":
            if move == "u":
                self.x -= 1
            if move == "d":
                self.x += 1

    def change_cords_by_value(self, X, Y):
        self.x = X
        self.y = Y

    def move(self):
        if self.left_bomb:
            self.left_bomb = False
        player_positions = self.where_is_player()

        if not self.is_bomb_there(player_positions[0]):
            if self.is_obstacle_there(player_positions[0]):
                self.leave_bomb()
                self.change_cords_by_value(self.last_x, self.last_y)
            else:
                self.last_x = self.x
                self.last_y = self.y
                self.change_cords(player_positions[0], player_positions[1])

        elif not self.is_bomb_there(player_positions[2]):
            if self.is_obstacle_there(player_positions[2]):
                self.leave_bomb()
                self.change_cords_by_value(self.last_x, self.last_y)
            else:
                self.last_x = self.x
                self.last_y = self.y
                self.change_cords(player_positions[2], player_positions[1])

        elif not self.is_bomb_there(player_positions[1]):
            if self.is_obstacle_there(player_positions[1]):
                self.leave_bomb()
                self.change_cords_by_value(self.last_x, self.last_y)
            else:
                self.last_x = self.x
                self.last_y = self.y
                self.change_cords(player_positions[1], player_positions[0])

        elif not self.is_bomb_there(player_positions[3]):
            if self.is_obstacle_there(player_positions[3]):
                self.leave_bomb()
                self.change_cords_by_value(self.last_x, self.last_y)
            else:
                self.last_x = self.x
                self.last_y = self.y
                self.change_cords(player_positions[3], player_positions[0])
