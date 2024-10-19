from Elements.Element import Element
from Util.Color import *


class Food(Element):

    def __init__(self, world, pos):
        super().__init__(world, pos)
        self.energy = 1
        self.color = Color(0.3)

    def be_eaten(self):
        self.world.remove(self)

    def get_energy(self):
        return self.energy

    def update(self):
        self.render()
