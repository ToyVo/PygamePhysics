from typing import Tuple, List

from Forces.Bond import Bond
from Objects.Particle import Particle
from Vec2 import Vec2


class Spring(Bond):
    def __init__(self, pair_list: List[Tuple[Particle, Particle]], k=1, length=1, d=1):
        super().__init__(pair_list)
        self.k = k
        self.length = length
        self.d = d

    def force(self, a: Particle, b: Particle) -> Vec2:
        s = a.pos - b.pos
        s_hat = s.hat()
        return -self.k * (s - self.length * s_hat) - self.d * ((a.vel - b.vel) @ s_hat) * s_hat
