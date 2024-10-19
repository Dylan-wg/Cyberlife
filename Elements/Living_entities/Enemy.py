from Elements.Element import Element
from Elements.Living_entities.Living_entity import Living_entity
from Elements.Living_entities.Moving_entity import Moving_entity
from Util.Action import DAMAGING
from Util.Vision import ALL


class Enemy(Moving_entity):

    def __init__(self, world, pos):
        super().__init__(world, pos)
        self.target = None
        self.damage_value = 0

    def damage(self, value):
        self.health -= value
        if self.health <= 0:
            self.world.remove(self)

    def get_damage_value(self):
        return self.damage_value

    def get_surroundings(self, distance) -> list[Element]:
        p = []
        for i in range(-distance, distance + 1):
            for j in range(-distance, distance + 1):
                p.append([i, j])
        ps = []
        for k in p:
            ps.append([self.pos[0] + k[0], self.pos[1] + k[1]])
        ps.remove(self.pos)
        for k in [1, -1]:
            for h in [1, -1]:
                ps.remove([self.pos[0] + distance * k, self.pos[1] + distance * h])
        r = []
        for j in self.world.get_elements():
            if j.get_pos() in ps:
                r.append(j)
        return r

    def attack(self):
        for i in self.get_surroundings(1):
            if isinstance(i, self.target) and isinstance(i, Living_entity):
                i.damage(self.damage_value)

    def is_target_exist(self) -> bool:
        if self.vision == ALL:
            for i in self.world.get_elements():
                if isinstance(i, self.target):
                    return True
            return False

    def get_target(self):
        return self.target
