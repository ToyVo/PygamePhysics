from typing import Tuple

from Objects.Circle import Circle
from Vec2 import Vec2


def circle_circle(a: Circle, b: Circle) -> Tuple[Circle, Circle, float, Vec2, Vec2]:
    r: Vec2 = a.pos - b.pos
    r_mag: float = r.mag()
    d: float = a.radius + b.radius - r_mag
    n: Vec2 = r.hat()
    p: Vec2 = a.pos + n * a.radius
    return a, b, d, n, p
