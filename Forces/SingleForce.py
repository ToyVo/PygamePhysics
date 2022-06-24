from typing import List

from Objects.Particle import Particle
from Vec2 import Vec2


class SingleForce:
    def __init__(self, particle_list: List[Particle]):
        self.particle_list = particle_list

    def force(self, o: Particle) -> Vec2:
        return Vec2()

    def apply(self) -> None:
        for o in self.particle_list:
            o.add_force(self.force(o))

    def remove(self, o: Particle) -> None:
        try:
            self.particle_list.remove(o)
        except ValueError:
            pass
