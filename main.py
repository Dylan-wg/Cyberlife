import random
import sys
import threading
from random import choice

import pygame
from Elements.Foods.Food import Food
from Elements.Living_entities.Cyberlife import Cyberlife
from Monitors.Monitor import Monitor
from World.World import World
from Elements.Living_entities.Enemy_zero import Enemy_zero


def main():
    world = World()
    cyberlife = Cyberlife(world, choice(world.get_available_pos()))
    world.add(cyberlife)
    monitor = Monitor(cyberlife, "Cyberlife")

    world.render()

    def get_food_num():
        r = 0
        for e in world.get_elements():
            if isinstance(e, Food):
                r += 1
        return r

    def get_enemy_num():
        r = 0
        for e in world.get_elements():
            if isinstance(e, Enemy_zero):
                r += 1
        return r

    # Main loop
    pygame.display.set_caption("Cyberlife")
    clock = pygame.time.Clock()
    pre_t = pygame.time.get_ticks()
    running = True
    while running:
        cur_t = pygame.time.get_ticks()
        if cur_t - pre_t >= 150:
            world.update()
            monitor.update()

            if get_food_num() <= 1:
                while get_food_num() < 3:
                    pos = choice(world.get_available_pos())
                    world.add(Food(world, pos))

            if get_enemy_num() < 1:
                b = random.choices([True, False], [0.1, 0.9])
                if b[0]:
                    ps = world.get_available_pos()
                    cyberlife_surrounding = [
                        [cyberlife.get_pos()[0] + 1, cyberlife.get_pos()[1]],
                        [cyberlife.get_pos()[0] - 1, cyberlife.get_pos()[1]],
                        [cyberlife.get_pos()[0], cyberlife.get_pos()[1] + 1],
                        [cyberlife.get_pos()[0], cyberlife.get_pos()[1] - 1]
                    ]
                    for i in cyberlife_surrounding:
                        if i in ps:
                            ps.remove(i)
                    pos = choice(ps)
                    world.add(Enemy_zero(world, pos))
                world.render()

            pre_t = cur_t
            clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


if __name__ == "__main__":
    main()
