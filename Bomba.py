class Bomb:
    def __init__(self, x, y, start, owner):
        self.x = x
        self.y = y
        self.exploded = False
        self.start = start
        self.owner = owner

    def boom(self):
        self.exploded = True
