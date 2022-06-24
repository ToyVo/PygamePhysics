import math
from typing import List, Tuple

import pygame

from Functions import center_of_line
from Objects.Particle import Particle
from Vec2 import Vec2


class Polygon(Particle):
    def __init__(self, pos: Vec2, offsets: List[Vec2], mass: float = float("inf"), vel: Vec2 = Vec2(), angle: float = 0,
                 avel: float = 0, momi: float = float("inf"), width: float = 0, color: Tuple[int, int, int] = None,
                 draw_normals: bool = False):

        self.draw_normals: bool = draw_normals

        # list of displacements to reach the vertices
        if offsets is None:
            offsets = []
        self.offsets: List[Vec2] = offsets

        self.points: List[Vec2] = []
        self.normals: List[Vec2] = []
        self.original_normals: List[Vec2] = []

        for o in self.offsets:
            p = self.pos + o
            self.points.append(p)

        for i in range(len(self.points)):
            n = -~(self.points[i] - self.points[i - 1]).hat()
            self.normals.append(n)
            self.original_normals.append(n)

        # check for convexity and if normals are facing out
        for i in range(len(self.offsets)):
            neg = 0
            pos = 0
            for j in range(len(self.offsets)):
                if not (i == j or i - 1 == j):
                    d = (self.offsets[j] - self.offsets[i]) @ self.normals[i]
                    if d < -1e-13:
                        neg += 1
                    elif d > 1e-13:
                        pos += 1
            if pos > 0:
                if neg == 0:
                    self.normals[i] *= -1
                else:
                    raise (ValueError, "Defined polygon is not convex.")

        super().__init__(mass=mass, pos=pos, vel=vel, angle=angle, avel=avel, momi=momi, color=color, width=width)

    def draw(self, screen) -> None:
        int_points = []
        for p in self.points:
            int_points.append(p.int())
        pygame.draw.polygon(screen, self.color, int_points, self.width)
        if self.draw_normals:
            for i in range(len(self.normals)):
                start = center_of_line(self.points[i], self.points[i - 1])
                end = (start + 50 * self.normals[i])
                pygame.draw.line(screen, (0, 0, 0), start.int(), end.int())

    def update(self, dt) -> None:
        super().update(dt)
        self.update_points_normals()

    def add_translate(self, displacement: Vec2):
        super().add_translate(displacement)
        self.update_points_normals()

    def update_points_normals(self):
        s = math.sin(self.angle)
        c = math.cos(self.angle)

        for i in range(len(self.points)):
            self.points[i] = self.pos + self.offsets[i].rotate_sin_cos(s, c)
            self.normals[i] = self.original_normals[i].rotate_sin_cos(s, c)
