class Shape:
    def __init__(self, shape: list[list], name: str = None):
        self.shape = shape
        self.name = name

    def __str__(self):
        if self.name is None:
            return self.shape
        else:
            return self.name

    def get_shape(self):
        return self.shape


POINT = Shape([[0, 0]], "point")
