from typing import Tuple, List

import pygame

from Objects.Particle import Particle
from Vec2 import Vec2


class Bond:
    def __init__(self, pair_list: List[Tuple[Particle, Particle]]):
        self.pair_list = pair_list

    def force(self, a: Particle, b: Particle) -> Vec2:
        return Vec2()

    def apply(self) -> None:
        for pair in self.pair_list:
            a, b = pair
            force = self.force(a, b)
            a.add_force(force)
            b.add_force(-force)

    def draw(self, screen, line_color: Tuple[int] = (0, 0, 0), line_width: float = 1) -> None:
        for pair in self.pair_list:
            a, b = pair
            pygame.draw.line(screen, line_color, a.pos, b.pos, line_width)

    def remove(self, o: Particle) -> None:
        remove: List[Tuple[Particle, Particle]] = []
        for pair in self.pair_list:
            a, b = pair
            if a == o or b == o:
                remove.append(pair)

        for pair in remove:
            self.pair_list.remove(pair)
