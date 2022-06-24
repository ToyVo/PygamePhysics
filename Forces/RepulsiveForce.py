from typing import List

from Contact.circle_circle import circle_circle
from Contact.circle_wall import circle_wall
from Forces.PairForce import PairForce
from Objects.Circle import Circle
from Objects.Particle import Particle
from Objects.Wall import Wall
from Vec2 import Vec2


class Repulsive(PairForce):
    def __init__(self, particle_list: List[Particle], strength: float = 10, length: float = 30):
        super().__init__(particle_list)
        self.strength = strength
        self.length = length

    def force(self, a: Particle, b: Particle) -> Vec2:
        if isinstance(a, Circle) and isinstance(b, Circle):
            _a, _b, d, n, p = circle_circle(a, b)
        elif isinstance(a, Circle) and isinstance(b, Wall):
            _a, _b, d, n, p = circle_wall(circle=a, wall=b)
        elif isinstance(a, Wall) and isinstance(b, Circle):
            _a, _b, d, n, p = circle_wall(circle=b, wall=a)
        else:
            return Vec2()

        if abs(d) > self.length:
            return Vec2()

        return self.strength * abs(d) * n
