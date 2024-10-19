import copy

from Util.Action import Action, NO_ACTION
from Util.Color import *
from Util.Shape import POINT


class Element:

    def __init__(self, world, pos=None):
        from World import World
        if pos is None:
            pos = [0, 0]
        self.world: World = world
        self.pos = pos
        self.color = WHITE
        self.shape = POINT
        self.tick: int = 0
        self.expected_action = NO_ACTION

    def get_world(self):
        return self.world

    def render(self):
        for i in self.shape.get_shape():
            self.world.set([self.pos[0] + i[0], self.pos[1] + i[1]], self.color.get_tuple())

    def update(self):
        self.tick += 1

    def get_pos(self):
        return self.pos

    def get_color(self):
        return self.color

    def get_tick(self):
        return self.tick

    def get_expected_action(self):
        return self.expected_action

    def set_expected_action(self, action: Action):
        self.expected_action = action

    def get_data(self):
        return {"Default": "None"}
