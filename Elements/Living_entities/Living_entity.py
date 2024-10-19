import math
from Elements.Element import Element
from Util.Vision import ALL


class Living_entity(Element):

    def __init__(self, world, pos):
        super().__init__(world, pos)
        self.health = math.inf
        self.vision = ALL

    def damage(self, value):
        self.health -= value
