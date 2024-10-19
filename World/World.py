import pygame
from Elements.Element import Element
from Util.Color import *


class World:

    def __init__(self):
        self.screen = None
        self.size = (4, 4)
        self.elements: list[Element] = []

    def add(self, element):
        if isinstance(element, Element):
            self.elements.append(element)

    def remove(self, element):
        if isinstance(element, Element):
            self.elements.remove(element)

    def render(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.size[0] * 10, self.size[1] * 10))
        for i in range(0, self.size[0] * 10):
            for j in range(0, self.size[1] * 10):
                self.screen.set_at((i, j), WHITE.get_tuple())
        try:
            for e in self.elements:
                e.render()
        except IndexError:
            pass

        pygame.display.flip()

    def update(self):
        for i in range(0, self.size[0] * 10):
            for j in range(0, self.size[1] * 10):
                self.screen.set_at((i, j), WHITE.get_tuple())
        for e in self.elements:
            if isinstance(e, Element):
                e.update()

        pygame.display.flip()

    def set(self, pos, color):
        for i in range(0, 10):
            for j in range(0, 10):
                self.screen.set_at((i + 10 * pos[0], j + 10 * pos[1]), color)

    def get_elements(self) -> list[Element]:
        return self.elements

    def get_available_pos(self) -> list[list[int, int]]:
        pos = []
        for i in range(0, self.size[0]):
            for j in range(0, self.size[1]):
                pos.append([i, j])
        for e in self.elements:
            pos.remove(e.get_pos())
        return pos
