import threading

from Elements.Element import Element
from Util.Brain import Brain
from Util.Color import *
from Elements.Living_entities import Enemy
from Elements.Foods.Food import Food
from Elements.Living_entities.Moving_entity import Moving_entity
from Util.Direction import *


class Cyberlife(Moving_entity):

    def __init__(self, world, pos):
        super().__init__(world, pos)
        self.color = BLACK
        self.brain = Brain(self, "cyberlife_brain")

    def eat(self):
        r = FAIL
        for i in self.get_surroundings(1):
            if isinstance(i, Food):
                i.be_eaten()
                r = EATING
        return r

    def attack(self):
        r = FAIL
        for i in self.get_surroundings(2):
            if isinstance(i, Enemy.Enemy):
                if isinstance(self, i.get_target()):
                    i.damage(1)
                    r = ATTACKING
        return r

    def damage(self, value):
        r = PASS
        for i in self.get_surroundings(1):
            if isinstance(i, Enemy.Enemy):
                if isinstance(self, i.get_target()):
                    r = DAMAGING
        return r

    def get_surroundings(self, distance) -> list[Element]:
        p = []
        for i in range(-distance, distance + 1):
            for j in range(-distance, distance + 1):
                p.append([i, j])
        ps = []
        for k in p:
            ps.append([self.pos[0] + k[0], self.pos[1] + k[1]])
        ps.remove(self.pos)
        if distance != 1:
            for k in [1, -1]:
                for h in [1, -1]:
                    ps.remove([self.pos[0] + distance * k, self.pos[1] + distance * h])
        r = []
        for j in self.world.get_elements():
            if j.get_pos() in ps:
                r.append(j)
        return r

    def think_to_action(self, action: Action):
        if action == NO_ACTION:
            pass
        elif action == GOING_UP:
            self.walk(UP)
        elif action == GOING_DOWN:
            self.walk(DOWN)
        elif action == GOING_RIGHT:
            self.walk(RIGHT)
        elif action == GOING_LEFT:
            self.walk(LEFT)
        elif action == EATING:
            self.eat()
        elif action == ATTACKING:
            self.attack()

    def update(self):
        self.tick += 1

        # new_thread = threading.Thread(target=self.think_to_action, args=([self.brain.think()]))
        # new_thread.start()
        # new_thread.join()
        action = self.brain.think()
        self.brain.update_score()
        self.brain.update_buffer()
        self.brain.update_epsilon()
        self.think_to_action(action)
        # self.brain.train()
        # self.brain.special_train()

        self.render()

    def get_tick(self):
        return self.tick

    def get_data(self):
        r: dict = {"pos": str(self.get_pos()),
                   "Action": str(self.get_expected_action()),
                   "Epsilon": str(self.brain.epsilon),
                   "Score": str(self.brain.score),
                   "Policy": str(self.brain.policy),
                   "Going up": str(self.brain.result[0]),
                   "Going down": str(self.brain.result[1]),
                   "Going right": str(self.brain.result[2]),
                   "Going left": str(self.brain.result[3]),
                   "Eating": str(self.brain.result[4]),
                   "Attacking": str(self.brain.result[5])
                   }
        return r
