from typing import List, Tuple

from Objects.Polygon import Polygon
from Vec2 import Vec2


class UniformPolygon(Polygon):
    def __init__(self, offsets: List[Vec2], pos: Vec2, density: float = 1, draw_normals: bool = False,
                 vel: Vec2 = Vec2(), angle: float = 0, avel: float = 0, width: float = 0,
                 color: Tuple[int, int, int] = None, infinite_mass: bool = False):
        # compute
        mass = 0
        momi = 0
        temp_pos = Vec2(pos)
        for i in range(len(offsets)):
            ai = (1 / 2) * (offsets[i] % offsets[i - 1])
            mi = density * ai
            ii = (mi / 6) * (offsets[i].mag2() + offsets[i - 1].mag2() + offsets[i] @ offsets[i - 1])
            ri = (1 / 3) * (offsets[i] + offsets[i - 1])

            mass += mi
            momi += ii
            temp_pos += mi * ri

        temp_pos /= mass

        new_offsets = []
        for o in offsets:
            new_offsets.append(o - temp_pos)

        if mass < 0:
            mass *= -1
            momi *= -1

        momi -= mass * temp_pos.mag2()

        if infinite_mass:
            mass = float("inf")

        super().__init__(pos=pos, offsets=new_offsets, mass=mass, momi=momi, draw_normals=draw_normals, vel=vel,
                         angle=angle, avel=avel, width=width, color=color)
