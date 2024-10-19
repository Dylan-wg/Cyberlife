class Color:

    def __init__(self, k, name=None):
        self.k = k
        self.name = name
        self.color = 255 * (1 - k), 255 * (1 - k), 255 * (1 - k)

    def get_tuple(self):
        return self.color

    def get_k(self):
        return self.k

    def __str__(self):
        if self.name is None:
            return "grey " + str(self.k)
        else:
            return self.name


WHITE = Color(0, "white")
BLACK = Color(1, "black")
