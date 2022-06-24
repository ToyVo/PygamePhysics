from typing import List

from Forces.PairForce import PairForce
from Objects.Particle import Particle
from Vec2 import Vec2


class Gravitation(PairForce):
    def __init__(self, particle_list: List[Particle], g: float = 10):
        super().__init__(particle_list)
        self.g = g

    def force(self, a: Particle, b: Particle) -> Vec2:
        r = a.pos - b.pos
        return -self.g * a.mass * b.mass / r.mag2() * r.hat()
