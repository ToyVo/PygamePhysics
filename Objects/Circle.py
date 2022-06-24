from typing import Tuple

import pygame

from Objects.Particle import Particle
from Vec2 import Vec2


class Circle(Particle):

    def __init__(self, pos: Vec2, mass: float = float("inf"), vel: Vec2 = Vec2(), angle: float = 0, avel: float = 0,
                 momi: float = float("inf"), width: float = 0, color: Tuple[int, int, int] = None, radius: float = 1):
        self.radius: float = radius
        super().__init__(mass=mass, pos=pos, vel=vel, angle=angle, avel=avel, momi=momi, color=color, width=width)

    def draw(self, surface) -> None:
        pygame.draw.circle(surface, self.color, self.pos.int(), self.radius)

    def in_area(self, pos: Vec2):
        if (self.pos - pos).mag2() < self.radius ** 2:
            return True
        else:
            return False
