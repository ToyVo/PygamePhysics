from typing import Tuple

from Objects.Polygon import Polygon
from Objects.Wall import Wall
from Vec2 import Vec2


def polygon_wall(polygon: Polygon, wall: Wall) -> Tuple[Polygon, Wall, float, Vec2, Vec2]:
    overlap_distance: float = -float("inf")
    point_of_overlap: Vec2 = Vec2()

    for p in polygon.points:
        d = (wall.pos - p) @ wall.normal
        if d > overlap_distance:
            overlap_distance = d
            point_of_overlap = p

    return polygon, wall, overlap_distance, wall.normal, point_of_overlap
