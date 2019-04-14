class Player:
    def __init__(self, X, Y, ind):
        self.indeks = ind
        self.X = X
        self.Y = Y
        self.allive = True
        self.last_x = X
        self.last_y = Y

    def reset(self):
        self.X = 1
        self.Y = 1
        self.allive = True

    def move(self, dir):
        self.last_x = self.X
        self.last_y = self.Y
        if dir == 'l':
            self.X -= 1
        elif dir == 'r':
            self.X += 1
        elif dir == 'd':
            self.Y -= 1
        elif dir == 'u':
            self.Y += 1
