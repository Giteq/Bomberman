from GameParams import *


class Bomb:
    def __init__(self, x, y, start, owner):
        self.x = x
        self.y = y
        self.exploded = False
        self.start = start
        self.owner = owner
        self.boom_range = bomb_range

    def boom(self):
        self.exploded = True

    def get_cords_in_range(self):
        """
        :return: List of tuples with coordinates fields in bomb range.
        """
        ret = []
        for x in range(self.x - self.boom_range, self.x + self.boom_range + 1):
            ret.append((x, self.y))
        for y in range(self.y - self.boom_range, self.y + self.boom_range + 1):
            ret.append((self.x, y))

        return ret
