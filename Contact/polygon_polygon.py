from typing import Tuple

from Objects.Polygon import Polygon
from Vec2 import Vec2


def polygon_polygon(a: Polygon, b: Polygon) -> Tuple[Polygon, Polygon, float, Vec2, Vec2]:
    overlap_distance: float = float("inf")
    normal: Vec2 = Vec2()
    point_of_overlap: Vec2 = Vec2()
    # noinspection PyTypeChecker
    penetrator: Polygon = None
    # noinspection PyTypeChecker
    penetratee: Polygon = None

    for i in range(len(a.normals)):
        ap = a.points[i]
        n = a.normals[i]
        max_overlap: float = -float("inf")
        max_point = Vec2()
        for bp in b.points:
            d = (ap - bp) @ n
            if d > max_overlap:
                max_overlap = d
                max_point = bp

        if max_overlap < overlap_distance:
            overlap_distance = max_overlap
            penetrator = b
            penetratee = a
            point_of_overlap = max_point
            normal = n

    for i in range(len(b.normals)):
        bp = b.points[i]
        n = b.normals[i]
        max_overlap: float = -float("inf")
        max_point = Vec2()
        for ap in a.points:
            d = (bp - ap) @ n
            if d > max_overlap:
                max_overlap = d
                max_point = ap

        if max_overlap < overlap_distance:
            overlap_distance = max_overlap
            penetrator = a
            penetratee = b
            point_of_overlap = max_point
            normal = n

    return penetrator, penetratee, overlap_distance, normal, point_of_overlap
