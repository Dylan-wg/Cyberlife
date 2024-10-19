import math


class Vision:

    def __init__(self, size, pos):
        self.size = size
        self.pos = pos

    def __str__(self):
        return {"size": self.size, "pos": self.pos}


ALL = Vision(math.inf, None)
