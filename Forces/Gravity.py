from typing import List

from Forces.SingleForce import SingleForce
from Objects.Particle import Particle
from Vec2 import Vec2


class Gravity(SingleForce):
    def __init__(self, particle_list: List[Particle], g: Vec2 = Vec2(10, 0)):
        super().__init__(particle_list)
        self.g = g

    def force(self, o: Particle) -> Vec2:
        if o.mass != float("inf"):
            return o.mass * self.g
        else:
            return Vec2()
