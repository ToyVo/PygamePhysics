from typing import Tuple

import pygame

from Objects.Particle import Particle
from Vec2 import Vec2


class Wall(Particle):
    def __init__(self, normal: Vec2 = Vec2(1, 0), length: float = 1000, pos: Vec2 = Vec2(), width: float = 1,
                 color: Tuple[int, int, int] = None):
        self.normal: Vec2 = normal.hat()
        self.length: float = length
        super().__init__(mass=float("inf"), pos=pos, vel=Vec2(), angle=0, avel=0, momi=float("inf"), color=color,
                         width=width)

    def draw(self, screen) -> None:
        displacement = self.length * ~self.normal
        start = self.pos - displacement
        end = self.pos + displacement
        pygame.draw.line(screen, self.color, start.int(), end.int())
