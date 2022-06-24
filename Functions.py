import random
from typing import Tuple

from Vec2 import Vec2


def get_random_color() -> Tuple[int, int, int]:
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


def center_of_line(start: Vec2, end: Vec2) -> Vec2:
    x = (start.x + end.x) / 2
    y = (start.y + end.y) / 2
    return Vec2(x, y)


def length_of_line(start: Vec2, end: Vec2) -> float:
    length = (start - end).mag()
    return length
