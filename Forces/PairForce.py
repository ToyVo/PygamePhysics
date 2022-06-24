from itertools import combinations
from typing import List, Tuple

import pygame

from Objects.Particle import Particle
from Vec2 import Vec2


class PairForce:
    def __init__(self, particle_list: List[Particle]):
        self.particle_list = particle_list

    def force(self, a: Particle, b: Particle) -> Vec2:
        return Vec2()

    def apply(self) -> None:
        for a, b in combinations(self.particle_list, 2):
            force = self.force(a, b)
            a.add_force(force)
            b.add_force(-force)

    def remove(self, o: Particle) -> None:
        try:
            self.particle_list.remove(o)
        except ValueError:
            pass

    def draw(self, screen, line_color: Tuple[int, int, int] = (0, 0, 0), line_width: float = 1) -> None:
        for a, b in combinations(self.particle_list, 2):
            pygame.draw.line(screen, line_color, a.pos, b.pos, line_width)
