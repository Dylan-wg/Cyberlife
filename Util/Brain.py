import math
import random
import threading

import keras
import numpy as np
import copy

from keras import layers, models

from Elements.Foods.Food import Food
from Elements.Living_entities import Cyberlife
from Elements.Living_entities.Enemy import Enemy
from World.World import World
from Util.Direction import *
from Util.Action import *


class Brain:

    def __init__(self, host, name):

        self.name = name
        self.main_neural_network: models.Sequential = self.generate_neural_network()
        self.target_neural_network: models.Sequential = self.generate_neural_network()
        self.target_neural_network.set_weights(self.main_neural_network.get_weights())
        self.data_buffer: list = []
        self.label_buffer: list = []
        self.special_data: list = []
        self.special_label: list = []
        self.host: Cyberlife.Cyberlife = host
        self.reflection = [GOING_UP, GOING_DOWN, GOING_RIGHT, GOING_LEFT, EATING, ATTACKING]
        self.score: float = 100.0
        self.gamma = 0.3
        self.buffer_size = 5000
        self.train_frequency = 4
        self.target_update_frequency = 40
        self.pre_score = self.score
        self.epsilon = 0.99
        self.epsilon_min = 0.05
        self.epsilon_decay_rate = 0.998
        self.epsilon_update_frequency = 4
        self.result = [0, 0, 0, 0, 0, 0]
        self.policy = ""
        self.think_action = random.choice(self.reflection)
        self.learning_rate = 0.8
        self.big_train_frequency = 500
        self.min_food_distance = 7
        self.decrease_time = 0
        self.be_randomly = 0
        self.env = []
        self.pre_env = []
        self.pre_pre_env = []

        try:
            with open("./Util/brain_data/" + self.name + ".txt", "r") as f:
                self.epsilon = float(f.readline().strip())
        except Exception:
            pass

    def __str__(self):
        return self.name

    def generate_neural_network(self) -> models.Sequential:
        model = models.Sequential()

        # model.add(layers.Conv2D(32, (1, 1), activation="relu", input_shape=(4, 4, 1), padding="same"))
        # model.add(layers.MaxPooling2D((1, 1)))
        # model.add(layers.Conv2D(64, (2, 2), activation="relu", padding="same"))
        # model.add(layers.MaxPooling2D((1, 1)))
        # model.add(layers.Conv2D(128, (2, 2), activation="relu", padding="same"))
        # model.add(layers.MaxPooling2D((1, 1)))
        # model.add(layers.Flatten())

        # model.add(layers.Input(shape=(16,)))

        model.add(layers.Conv2D(32, (1, 1), activation="relu", input_shape=(3, 16, 1), padding="same"))
        model.add(layers.Flatten())

        model.add(layers.Dense(64, activation="relu"))
        model.add(layers.Dense(128, activation="relu"))
        model.add(layers.Dropout(0.5))
        model.add(layers.Dense(512, activation="sigmoid"))
        model.add(layers.Dropout(0.5))
        model.add(layers.Dense(64, activation="relu"))
        model.add(layers.Dense(6, activation="sigmoid"))

        optimizer = keras.optimizers.Adam(clipnorm=1.0, learning_rate=1e-3)
        model.compile(optimizer=optimizer, loss='mse', metrics=["accuracy"])

        # model.compile(optimizer="adam", loss="mean_squared_error", metrics=["accuracy"])

        try:
            model.load_weights("./Util/brain_data/" + self.name + ".weights.h5")
        except FileNotFoundError:
            pass

        return model

    def get_neural_network_summary(self):
        self.main_neural_network.summary()

    def think(self) -> Action:
        r = random.choice(self.reflection)
        choices = ["randomly", "maximum"]
        policy = random.choices(choices, [self.epsilon, 1 - self.epsilon])[0]
        if self.decrease_time >= 6:
            self.be_randomly = 3
        if self.decrease_time >= 6 or self.be_randomly > 0:
            # policy = "randomly"
            self.be_randomly = max([self.be_randomly - 1, 0])
        # policy = "randomly"
        self.policy = policy

        if policy == "maximum":
            e = self.get_formatted_environment()
            env = []
            world = self.host.get_world()
            for i in range(0, world.size[0]):
                for j in range(0, world.size[1]):
                    env.append(e[i][j])

            c_env = copy.deepcopy(env)
            env = [self.pre_pre_env, self.pre_env, self.env]
            for i in range(0, len(env)):
                if not env[i]:
                    env[i] = c_env

            result: list[6] = self.main_neural_network.predict(np.array([env]))[0]
            self.result = copy.deepcopy(result)
            ref = copy.deepcopy(self.reflection)
            result = list(result)
            for i in range(0, len(self.reflection)):
                r = ref[result.index(max(result))]
                if self.action_can_be_done(r):
                    break
                else:
                    ref.remove(r)
                    result.remove(max(result))
            if not ref:
                r = random.choice([GOING_UP, GOING_DOWN, GOING_RIGHT, GOING_LEFT])
            self.host.set_expected_action(r)
            self.think_action = r
        else:
            self.result = [0, 0, 0, 0, 0, 0]
            ref = copy.deepcopy(self.reflection)
            for i in range(0, len(self.reflection)):
                r = random.choice(ref)
                if self.action_can_be_done(r):
                    break
                else:
                    ref.remove(r)
            if not ref:
                r = random.choice([GOING_UP, GOING_DOWN, GOING_RIGHT, GOING_LEFT])
            self.host.set_expected_action(r)
            self.think_action = r
        return r

    def action_can_be_done(self, action: Action):
        if action == EATING:
            for i in self.host.get_surroundings(1):
                if isinstance(i, Food):
                    return True
        elif action == ATTACKING:
            for i in self.host.get_surroundings(2):
                if isinstance(i, Enemy):
                    if isinstance(self.host, i.get_target()):
                        return True
        elif action in [GOING_UP, GOING_DOWN, GOING_RIGHT, GOING_LEFT]:
            new_host_pos = copy.deepcopy(self.host.get_pos())
            if action == GOING_UP:
                new_host_pos[0] += UP.get_dx()
                new_host_pos[1] += UP.get_dy()
            elif action == GOING_DOWN:
                new_host_pos[0] += DOWN.get_dx()
                new_host_pos[1] += DOWN.get_dy()
            elif action == GOING_RIGHT:
                new_host_pos[0] += RIGHT.get_dx()
                new_host_pos[1] += RIGHT.get_dy()
            elif action == GOING_LEFT:
                new_host_pos[0] += LEFT.get_dx()
                new_host_pos[1] += LEFT.get_dy()
            if new_host_pos in self.host.get_world().get_available_pos():
                return True
        return False

    def get_world(self) -> World:
        return self.host.get_world()

    def get_formatted_environment(self):
        r = []
        world = self.get_world()
        for i in range(0, world.size[0]):
            ll = []
            for j in range(0, world.size[1]):
                ll.append(0)
            r.append(ll)
        for i in world.get_elements():
            pos = i.get_pos()
            try:
                r[pos[1]][pos[0]] = i.get_color().get_k()
            except IndexError:
                continue
        return r

    def get_formatted_environment_after_act(self, action: Action):
        origin = self.get_formatted_environment()
        r = copy.deepcopy(origin)
        if action == NO_ACTION:
            return origin
        elif action == EATING:
            for i in self.host.get_surroundings(1):
                if isinstance(i, Food):
                    r[i.get_pos()[1]][i.get_pos()[0]] = 0
            return r
        elif action == ATTACKING:
            for i in self.host.get_surroundings(2):
                if isinstance(i, Enemy):
                    r[i.get_pos()[1]][i.get_pos()[0]] = 0
            return r
        else:
            for i in self.host.shape.get_shape():
                try:
                    r[i[1] + self.host.get_pos()[1]][i[0] + self.host.get_pos()[0]] = 0
                except IndexError:
                    continue
            new_host_pos = copy.deepcopy(self.host.get_pos())
            if action == GOING_UP:
                new_host_pos[0] += UP.get_dx()
                new_host_pos[1] += UP.get_dy()
            elif action == GOING_DOWN:
                new_host_pos[0] += DOWN.get_dx()
                new_host_pos[1] += DOWN.get_dy()
            elif action == GOING_RIGHT:
                new_host_pos[0] += RIGHT.get_dx()
                new_host_pos[1] += RIGHT.get_dy()
            elif action == GOING_LEFT:
                new_host_pos[0] += LEFT.get_dx()
                new_host_pos[1] += LEFT.get_dy()
            for i in self.host.shape.get_shape():
                try:
                    r[i[1] + new_host_pos[1]][i[0] + new_host_pos[0]] = self.host.get_color().get_k()
                except IndexError:
                    continue
            return r

    def q(self, r, gamma, action: Action) -> list[6]:
        env = [self.pre_pre_env, self.pre_env, self.env]

        a_e = self.get_formatted_environment_after_act(action)
        a_env = []
        world = self.host.get_world()
        for i in range(0, world.size[0]):
            for j in range(0, world.size[1]):
                a_env.append(a_e[i][j])
        a_env = [self.pre_env, self.env, a_env]

        if r < 2 and self.decrease_time < 12:
            self.decrease_time += 1
        else:
            self.decrease_time -= 1

        target_q: list[6] = self.target_neural_network.predict(np.array([a_env]))[0]
        re = self.main_neural_network.predict(np.array([env]))[0]
        print(re)
        re[self.reflection.index(action)] = r + gamma * max(list(target_q))
        if r < 2:
            for i in range(0, len(re)):
                if self.reflection[i] != action and self.action_can_be_done(self.reflection[i]):
                    re[i] = max([re[i], 0.75 / (1 + math.e ** (-8.5 * (re[i] - 0.15)))])
        print(re)
        for i in range(0, len(re)):
            if self.reflection[i] == action:
                re[i] = 1 / (1 + math.e ** (-0.3 * (re[i] - 2)))
        for i in range(0, len(re)):
            if self.reflection[i] == action:
                re[i] = 1 / (1 + math.e ** (-15 * (re[i] - 0.6)))
                if r < 2:
                    re[i] = math.log((0.49 * re[i] + 0.5) / (0.5 - 0.49 * re[i])) * 0.12
            else:
                if r >= 2:
                    re[i] = math.log((0.49 * re[i] + 0.5) / (0.5 - 0.49 * re[i])) * 0.12
        print(re)
        re = list(re)
        return re

    def get_host_action(self):
        r = []
        for i in self.host.get_surroundings(1):
            if isinstance(i, Food) and self.action_can_be_done(self.think_action) and self.think_action == EATING:
                r.append(EATING)
        for i in self.host.get_surroundings(2):
            if isinstance(i, Enemy) and self.action_can_be_done(self.think_action) and self.think_action == ATTACKING:
                r.append(ATTACKING)
        if self.think_action in [GOING_UP, GOING_DOWN, GOING_RIGHT, GOING_LEFT]:
            if self.action_can_be_done(self.think_action):
                r.append(self.think_action)
        for i in self.host.world.get_elements():
            if isinstance(i, Enemy) and isinstance(self.host, i.get_target()):
                for j in i.get_surroundings(1):
                    if j == self.host:
                        r.append(DAMAGING)
        return r

    def update_score(self):
        h_action = self.get_host_action()
        self.pre_score = self.score
        if (not(EATING in h_action)) and (not(ATTACKING in h_action)):
            self.score -= 2
            k = 1
        else:
            k = 0
        if len(h_action) != 0:

            print([i.name for i in h_action])

            while len(h_action) != 0:
                self.score += h_action.pop().get_d_score()
        d = []
        p = self.host.get_pos()
        for i in self.host.get_world().get_elements():
            if isinstance(i, Food):
                if self.think_action in [GOING_UP, GOING_DOWN, GOING_RIGHT, GOING_LEFT] and self.action_can_be_done(self.think_action):
                    if self.think_action == GOING_UP:
                        d.append((((i.get_pos()[0] - p[0]) ** 2) + (i.get_pos()[1] - p[1] + 1) ** 2) ** 0.5)
                    elif self.think_action == GOING_DOWN:
                        d.append((((i.get_pos()[0] - p[0]) ** 2) + (i.get_pos()[1] - p[1] - 1) ** 2) ** 0.5)
                    elif self.think_action == GOING_RIGHT:
                        d.append((((i.get_pos()[0] - p[0] - 1) ** 2) + (i.get_pos()[1] - p[1]) ** 2) ** 0.5)
                    elif self.think_action == GOING_LEFT:
                        d.append((((i.get_pos()[0] - p[0] + 1) ** 2) + (i.get_pos()[1] - p[1]) ** 2) ** 0.5)
        if len(d) == 0:
            d.append(self.min_food_distance)
        if self.min_food_distance != min(d):
            delta = self.min_food_distance - min(d)
            self.min_food_distance = min(d)
            self.score += (20 * delta * k)
        elif self.min_food_distance == min(d):
            self.min_food_distance = min(d)
            self.score -= (10 * k)
        if self.host.pos == self.host.pre_pre_pos:
            self.score -= 3

    def update_buffer(self):
        e = self.get_formatted_environment()
        data = []
        world = self.host.get_world()
        for i in range(0, world.size[0]):
            for j in range(0, world.size[1]):
                data.append(e[i][j])

        label = []
        if self.host.tick > 3:
            label = self.q(self.score - self.pre_score, self.gamma, self.think_action)

        self.pre_pre_env = self.pre_env
        self.pre_env = self.env
        self.env = copy.deepcopy(data)

        if self.host.tick > 3:
            if not self.pre_env:
                self.pre_env = copy.deepcopy(self.env)
            if not self.pre_pre_env:
                self.pre_pre_env = copy.deepcopy(self.pre_env)

            data = [self.pre_pre_env, self.pre_env, self.env]

            if data in self.data_buffer or self.score - self.pre_score < 2:
                if data in self.special_data:
                    self.special_label[self.special_data.index(data)] = label
                else:
                    self.special_data.append(data)
                    self.special_label.append(label)

            if data in self.data_buffer:
                self.label_buffer[self.data_buffer.index(data)] = label
            else:
                if len(self.data_buffer) >= self.buffer_size:
                    self.data_buffer.pop(0)
                    self.label_buffer.pop(0)
                self.data_buffer.append(data)
                self.label_buffer.append(label)

    def update_epsilon(self):
        if self.host.tick % self.epsilon_update_frequency == 0:
            self.epsilon = max([self.epsilon_min, self.epsilon * self.epsilon_decay_rate])
            with open("./Util/brain_data/" + self.name + ".txt", "w") as f:
                f.write(str(self.epsilon))

    def train(self):
        print("-----------------------------------------------------------------------")
        print(len(self.label_buffer))
        print("-----------------------------------------------------------------------")
        if self.host.tick <= 3:
            return

        if self.host.get_tick() % self.train_frequency == 0:
            if self.host.get_tick() % self.big_train_frequency == 0:
                self.main_neural_network.fit(x=np.array(self.data_buffer), y=np.array(self.label_buffer), epochs=20,
                                             batch_size=150)
            else:
                self.main_neural_network.fit(x=np.array(self.data_buffer), y=np.array(self.label_buffer), epochs=5,
                                             batch_size=1500)
                # self.main_neural_network.fit(x=np.array(self.data_buffer[max([-5, -len(self.data_buffer)]):]),
                #                             y=np.array(self.label_buffer[max([-5, -len(self.label_buffer)]):]),
                #                             epochs=5,
                #                             batch_size=10)
            self.main_neural_network.save_weights("./Util/brain_data/" + self.name + ".weights.h5")
        if self.host.get_tick() % self.target_update_frequency == 0:
            self.target_neural_network.set_weights(self.main_neural_network.get_weights())

    def special_train(self):
        if self.special_data and self.special_label and self.host.tick % 10 == 0:
            self.main_neural_network.fit(x=np.array(self.special_data), y=np.array(self.special_label), epochs=50,
                                         batch_size=50)
