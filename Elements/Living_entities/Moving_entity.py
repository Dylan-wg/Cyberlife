from Elements.Living_entities.Living_entity import Living_entity
from Util.Direction import *


class Moving_entity(Living_entity):

    def __init__(self, world, pos):
        super().__init__(world, pos)
        self.pre_pos = None
        self.pre_pre_pos = None

    def walk(self, direction: Direction) -> Action:
        new_pos = [self.pos[0] + direction.get_dx(), self.pos[1] + direction.get_dy()]
        if new_pos in self.world.get_available_pos():
            self.pre_pre_pos = self.pre_pos
            self.pre_pos = self.pos
            self.pos = new_pos
            return direction.get_action()
        else:
            return FAIL
