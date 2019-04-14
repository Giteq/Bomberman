class Player:
    def __init__(self, x, y, ind):
        self.ind = ind
        self.x = x
        self.y = y
        self.alive = True
        self.last_x = x
        self.last_y = y

    def reset(self):
        self.x = 1
        self.y = 1
        self.alive = True

    def move(self , direction):
        self.last_x = self.x
        self.last_y = self.y
        if direction == 'l':
            self.x -= 1
        elif direction == 'r':
            self.x += 1
        elif direction == 'd':
            self.y -= 1
        elif direction == 'u':
            self.y += 1
