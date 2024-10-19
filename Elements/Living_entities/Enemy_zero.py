import math

from Elements.Living_entities.Cyberlife import Cyberlife
from Elements.Living_entities.Enemy import Enemy
from Util.Direction import *
from Util.Vision import ALL
from random import choice
from Util.Color import *


class Enemy_zero(Enemy):

    def __init__(self, world, pos):
        super().__init__(world, pos)
        self.target = Cyberlife
        self.vision = ALL
        self.health = 1
        self.color = Color(0.6)
        self.damage_value = 1
        self.memory: dict[tuple: int] = {}  # unavailable pos
        self.memory_duration = 10

    def choose_direction(self) -> Direction:
        if not self.is_target_exist():
            return choice(DIRECTIONS)

        attk_target = None
        min_dis = math.inf
        for i in self.world.get_elements():
            if isinstance(i, self.target):
                dis = ((i.get_pos()[0] - self.pos[0]) ** 2 + (i.get_pos()[1] - self.pos[1]) ** 2) ** 0.5
                if dis <= min_dis:
                    min_dis = dis
                    attk_target = i

        dy = attk_target.get_pos()[1] - self.pos[1]
        dx = attk_target.get_pos()[0] - self.pos[0]
        if [dx, dy] == [1, 0] or [dx, dy] == [-1, 0] or [dx, dy] == [0, 1] or [dx, dy] == [0, -1] or [dx, dy] == [0, 0]\
                or self.get_available_directions() == []:
            return NONE

        cos = dx / ((dx ** 2 + dy ** 2) ** 0.5)
        a_pos = self.world.get_available_pos()
        queue = [NONE]
        if (2 ** 0.5) / 2 < cos <= 1:
            if dy < 0:
                queue = [RIGHT, UP, LEFT, DOWN]
            else:  # dy >= 0
                queue = [RIGHT, DOWN, LEFT, UP]
        elif -1 <= cos < -(2 ** 0.5) / 2:
            if dy < 0:
                queue = [LEFT, UP, RIGHT, DOWN]
            else:  # dy >= 0
                queue = [LEFT, DOWN, RIGHT, UP]
        elif -(2 ** 0.5) / 2 <= cos <= (2 ** 0.5) / 2:
            if dy <= 0:
                if dx > 0:
                    queue = [UP, RIGHT, LEFT, DOWN]
                else:  # dx <= 0
                    queue = [UP, LEFT, RIGHT, DOWN]
            elif dy > 0:
                if dx > 0:
                    queue = [DOWN, RIGHT, LEFT, UP]
                else:  # dx <= 0
                    queue = [DOWN, LEFT, RIGHT, UP]

        r = NONE
        for d in queue:
            if (self.get_pos_after_walk(d) in a_pos) and (not(tuple(self.get_pos_after_walk(d)) in self.memory)):
                r = d
                if queue.index(r) != 0:
                    self.memory[tuple(self.pos)] = self.memory_duration
                break

        return r

    def update_memory(self):
        for i in self.memory:
            self.memory[i] -= 1
        keys = []
        for i in self.memory:
            if self.memory[i] < 0:
                keys.append(i)
        for i in keys:
            self.memory.pop(i)

    def update(self):
        # print(self.pos)
        # print(self.memory)
        self.update_memory()
        self.attack()
        self.walk(self.choose_direction())
        self.render()

    def get_available_directions(self):
        r = []
        for d in DIRECTIONS:
            if [self.pos[0] + d.get_dx(), self.pos[1] + d.get_dy()] in self.world.get_available_pos():
                r.append(d)
        return r

    def get_pos_after_walk(self, direction: Direction) -> list[int, int]:
        return [self.pos[0] + direction.get_dx(), self.pos[1] + direction.get_dy()]
