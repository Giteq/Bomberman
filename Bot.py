from Player import Player


class Bot(Player):
    def __init__(self, X, Y, ind):
        super().__init__(X, Y, ind)
        self.left_bomb = False
        self.players = []
        self.board = []
        self.left_bomb = False
        self.MAP_WIDTH = 24
        self.MAP_HEIGHT = 24

    def reset(self):
        self.X = 1
        self.Y = 1
        self.allive = True

    def remember_board(self, board):
        self.board = board

    def remember_player_pos(self, players):
        self.players = players

    def remember_bombs(self, bombs):
        self.bombs = bombs

    def is_bomb_there(self , dir):

        if dir == "r":
            if self.X + 2 < self.MAP_WIDTH and self.Y + 1 < self.MAP_WIDTH and self.X > 0 and self.Y > 0:
                if self.board[self.X+1][self.Y+1] == "XX" or self.board[self.X+2][self.Y] == "XX" or self.board[self.X+1][self.Y-1] == "XX" or \
                        self.board[self.X+1][self.Y] == "XX" or self.board[self.X+1][self.Y] == "##" or self.board[self.X][self.Y] == "XX":
                    return True
        if dir == "l":
            if self.X - 2 < self.MAP_WIDTH and self.Y + 1 < self.MAP_WIDTH and self.X > 0 and self.Y > 0:
                if self.board[self.X-1][self.Y+1] == "XX" or self.board[self.X-2][self.Y] == "XX" or self.board[self.X-1][self.Y-1] == "XX" or \
                        self.board[self.X - 1][self.Y] == "XX" or self.board[self.X-1][self.Y] == "##" or self.board[self.X][self.Y] == "XX":
                    return True
        if dir == "u":
            if self.Y - 2 < self.MAP_WIDTH and self.X + 1 < self.MAP_WIDTH and self.X > 0 and self.Y > 0:
                if self.board[self.X][self.Y-2] == "XX" or self.board[self.X+1][self.Y-1] == "XX" or self.board[self.X-1][self.Y-1] == "XX" or \
                    self.board[self.X][self.Y - 1]== "XX" or self.board[self.X][self.Y-1] == "##" or self.board[self.X][self.Y] == "XX":
                    return True
        if dir == "d":
            if self.Y + 2 < self.MAP_WIDTH and self.X + 1 < self.MAP_WIDTH and self.X > 0 and self.Y > 0:
                if self.board[self.X+1][self.Y+1] == "XX" or self.board[self.X][self.Y+2] == "XX" or self.board[self.X-1][self.Y+1] == "XX" or \
                    self.board[self.X][self.Y+1]== "XX" or self.board[self.X][self.Y+1] == "##" or self.board[self.X][self.Y] == "XX":
                    return True

        return False

    def where_is_player(self):
        ret_val = []

        if self.players[0].X < self.X:
            ret_val.append("l")
            ret_val.append("r")
        if self.players[0].X > self.X:
            ret_val.append("r")
            ret_val.append("l")
        if self.players[0].Y > self.Y:
            ret_val.append("d")
            ret_val.append("u")
        if self.players[0].Y < self.Y:
            ret_val.append("u")
            ret_val.append("d")
        if self.players[0].X == self.X:
            ret_val.append("e")
            if self.players[0].Y > self.Y:
                ret_val.append("u")
            if self.players[0].Y < self.Y:
                ret_val.append("d")
        if self.players[0].Y == self.Y:
            if self.players[0].X > self.X:
                ret_val.append("r")
            if self.players[0].X < self.X:
                ret_val.append("l")
            ret_val.append("e")

        return ret_val

    def is_obstacle_there(self, dir):
        if dir == "r":
            if self.board[self.X + 1][self.Y] == "**":
                return True
        if dir == "l":
            if self.board[self.X - 1][self.Y] == "**":
                return True
        if dir =="u":
            if self.board[self.X][self.Y - 1] == "**":
                return True
        if dir == "d":
            if self.board[self.X][self.Y + 1] == "**":
                return True
        return False

    def leave_bomb(self):
        self.left_bomb = True

    def is_bomb_left(self):
        return self.left_bomb

    def change_cords(self, move, move2):
        if move == "r":
            self.X +=1
        if move  == "l":
            self.X -= 1
        if move == "u":
            self.Y -= 1
        if move == "d":
            self.Y += 1
        if move == "e":
            if move2 == "l":
                self.Y -= 1
            if move2 == "r":
                self.Y += 1
        if move2 == "e":
            if move == "u":
                self.X -= 1
            if move == "d":
                self.X += 1



    def change_cords_by_value(self, X, Y):
        self.X = X
        self.Y = Y

    def move(self):
        if self.left_bomb:
            self.left_bomb = False

        #lista najpierw prawo/lewo potem gora/dol "e" jesli rowne
        player_positions = self.where_is_player()

        if not self.is_bomb_there(player_positions[0]):
            if self.is_obstacle_there(player_positions[0]):
                self.leave_bomb()
                self.change_cords_by_value(self.last_x , self.last_y)
            else:
                self.last_x = self.X
                self.last_y = self.Y
                self.change_cords(player_positions[0], player_positions[1])

        elif not self.is_bomb_there(player_positions[2]):
            if self.is_obstacle_there(player_positions[2]):
                self.leave_bomb()
                self.change_cords_by_value(self.last_x , self.last_y)
            else:
                self.last_x = self.X
                self.last_y = self.Y
                self.change_cords(player_positions[2], player_positions[1])

        elif not self.is_bomb_there(player_positions[1]):
            if self.is_obstacle_there(player_positions[1]):
                self.leave_bomb()
                self.change_cords_by_value(self.last_x , self.last_y)
            else:
                self.last_x = self.X
                self.last_y = self.Y
                self.change_cords(player_positions[1], player_positions[0])

        elif not self.is_bomb_there(player_positions[3]):
            if self.is_obstacle_there(player_positions[3]):
                self.leave_bomb()
                self.change_cords_by_value(self.last_x , self.last_y)
            else:
                self.last_x = self.X
                self.last_y = self.Y
                self.change_cords(player_positions[3], player_positions[0])
