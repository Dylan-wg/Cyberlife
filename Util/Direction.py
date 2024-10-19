from Util.Action import *


class Direction:

    def __init__(self, name):
        self.action = NO_ACTION
        self.dy = self.dx = 0
        self.name = name

    def __str__(self):
        return self.name

    def set_dx(self, dx):
        self.dx = dx

    def get_dx(self):
        return self.dx

    def set_dy(self, dy):
        self.dy = dy

    def get_dy(self):
        return self.dy

    def set_action(self, action: Action):
        self.action = action

    def get_action(self) -> Action:
        return self.action


NONE = Direction("None")

UP = Direction("up")
UP.set_dy(-1)
UP.set_action(GOING_UP)

DOWN = Direction("DOWN")
DOWN.set_dy(1)
DOWN.set_action(GOING_DOWN)

RIGHT = Direction("RIGHT")
RIGHT.set_dx(1)
RIGHT.set_action(GOING_RIGHT)

LEFT = Direction("LEFT")
LEFT.set_dx(-1)
LEFT.set_action(GOING_LEFT)

DIRECTIONS = (NONE, UP, DOWN, RIGHT, LEFT)
