from typing import List

from Forces.SingleForce import SingleForce
from Objects.Circle import Circle
from Objects.Particle import Particle
from Vec2 import Vec2


class AirDrag(SingleForce):
    def __init__(self, particle_list: List[Particle], d=1, wind=Vec2()):
        super().__init__(particle_list)
        self.d = d
        self.wind = wind

    def force(self, o: Circle) -> Vec2:
        vel = o.vel - self.wind
        return -2 * self.d * o.radius * vel.mag() * vel
