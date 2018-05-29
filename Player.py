class Player:
    def __init__(self, X, Y, ind):
        self.indeks = ind
        self.X = X
        self.Y = Y
        self.zywy = True
        self.wczesniejsze_x = X
        self.wczesniejsze_y = Y
    def reset(self):
        self.X = 1
        self.Y = 1
        self.zywy = True