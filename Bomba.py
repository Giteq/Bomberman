class Bomba:
    def __init__(self, X, Y, start, wlasciciel):
        self.X = X
        self.Y = Y
        self.wybuchnieta = False
        self.start = start
        self.wlasciciel = wlasciciel
    def wybucham(self):
        self.wybuchnieta = True