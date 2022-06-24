from typing import Tuple

from Functions import get_random_color
from Vec2 import Vec2


class Particle:
    def __init__(self, mass: float, pos: Vec2, vel: Vec2, angle: float, avel: float, momi: float, width: float,
                 color: Tuple[int, int, int]):
        self.mass: float = mass
        self.pos: Vec2 = Vec2(pos)
        self.vel: Vec2 = Vec2(vel)
        self.force: Vec2 = Vec2()
        self.angle: float = angle
        self.avel: float = avel
        self.momi: float = momi
        self.torque: float = 0
        if color is None:
            color = get_random_color()
        self.color: Tuple[int, int, int] = color
        self.width = width

    def update(self, dt: float) -> None:
        self.vel += (self.force / self.mass) * dt
        self.pos += self.vel * dt
        self.avel += (self.torque / self.momi) * dt
        self.angle += self.avel * dt

    def clear_force(self) -> None:
        self.force = Vec2()

    def clear_torque(self) -> None:
        self.torque = 0

    def add_force(self, force: Vec2, pos: Vec2 = None) -> None:
        self.force += force
        if pos is not None:
            self.torque += (pos - self.pos) % self.force

    def add_translate(self, displacement: Vec2):
        self.pos += displacement

    def add_torque(self, torque) -> None:
        self.torque += torque

    def draw(self, screen) -> None:
        pass

    def add_impulse(self, impulse: Vec2, pos: Vec2 = None):
        self.vel += impulse / self.mass
        if pos is not None:
            self.avel += (pos - self.pos) % impulse / self.momi

    def in_area(self, pos: Vec2):
        pass
