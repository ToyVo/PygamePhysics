from typing import Tuple

from Objects.Circle import Circle
from Objects.Wall import Wall
from Vec2 import Vec2


def circle_wall(circle: Circle, wall: Wall) -> Tuple[Circle, Wall, float, Vec2, Vec2]:
    n: Vec2 = wall.normal
    d: float = (wall.pos - circle.pos) @ n + circle.radius
    p: Vec2 = circle.pos - n * circle.radius
    return circle, wall, d, n, p
