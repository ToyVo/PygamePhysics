from typing import Tuple

from Objects.Circle import Circle
from Objects.Polygon import Polygon
from Vec2 import Vec2


def circle_polygon(circle: Circle, polygon: Polygon) -> Tuple[Circle, Polygon, float, Vec2, Vec2]:
    distance: float = float("inf")
    normal: Vec2 = Vec2()
    point_of_overlap = Vec2()

    for i in range(len(polygon.points)):
        n = polygon.normals[i]
        d = (polygon.points[i] - circle.pos) @ n + circle.radius
        if d < distance:
            distance = d
            normal = n
            point_of_overlap = circle.pos - n * circle.radius
    return circle, polygon, distance, normal, point_of_overlap
