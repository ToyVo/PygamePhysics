from itertools import combinations
from typing import List, Tuple

import pygame

from Contact.circle_circle import circle_circle
from Contact.circle_polygon import circle_polygon
from Contact.circle_wall import circle_wall
from Contact.polygon_polygon import polygon_polygon
from Contact.polygon_wall import polygon_wall
from Objects.Circle import Circle
from Objects.Particle import Particle
from Objects.Polygon import Polygon
from Objects.Wall import Wall
from Vec2 import Vec2


def handle_contact(particle_list: List[Particle], restitution: float = 1) -> None:
    contacts_handled: int = 0
    max_contacts_handled: int = 4 * len(particle_list)
    while contacts_handled < max_contacts_handled:
        handled_this_round: int = 0
        for a, b in combinations(particle_list, 2):
            handled_this_round += contact(a, b, restitution=restitution)
        if handled_this_round == 0:
            break
        contacts_handled += handled_this_round


def bounce(contact_data: Tuple[Particle, Particle, float, Vec2, Vec2], restitution: float = 0) -> int:
    if contact_data is not None:
        a: Particle
        b: Particle
        d: float
        n: Vec2
        p: Vec2

        a, b, d, n, p = contact_data

        if d > 0:
            # find inverse masses
            mia = 1 / a.mass
            mib = 1 / b.mass

            # if both masses are infinity, make them equal
            if mia == 0 and mib == 0:
                if isinstance(a, Wall) or isinstance(b, Wall):
                    return 0
                mia = 1
                mib = 1
                m = 1
            else:
                m = 1 / (mia + mib)  # reduced mass

            # resolve overlap
            s = m * d * n
            a.add_translate(s * mia)
            b.add_translate(-s * mib)

            n_hat = n.hat()

            sa = p - a.pos
            sb = p - b.pos

            # resolve velocity
            v = (a.vel + a.avel * ~sa) - (b.vel + b.avel * ~sb)
            vn = v @ n
            if vn < 0:
                t_hat = ~n

                vt = v @ t_hat

                san = sa @ n
                sbn = sb @ n
                sat = sa @ t_hat
                sbt = sb @ t_hat

                mnn = mia + mib + san ** 2 / a.momi + sbn ** 2 / b.momi
                mtt = mia + mib + sat ** 2 / a.momi + sbt ** 2 / b.momi
                mnt = san * sat / a.momi + sbn * sbt / b.momi
                delta_vn = -(1 + restitution) * vn
                delta_vt = -2 * vt

                jn = (1 / (mnn * mtt - mnt ** 2)) * (mnn * delta_vn + mnt * delta_vt)
                jt = (1 / (mnn * mtt - mnt ** 2)) * (mnt * delta_vn + mtt * delta_vt)

                j = jn * n_hat + jt * t_hat

                a.add_impulse(j, p)
                b.add_impulse(-1 * j, p)
            return 1
    return 0


def draw_overlap(screen, poly1, poly2):
    a: Particle
    b: Particle
    d: float
    n: Vec2
    p: Vec2

    a, b, d, n, p = polygon_polygon(poly1, poly2)

    if d > 0:
        screen.fill((255, 255, 0))
        pygame.draw.circle(screen, (0, 0, 0), p.int(), 5)
        pygame.draw.line(screen, (0, 0, 0), p.int(), (p + n * d).int())


def contact(a, b, restitution) -> int:
    if isinstance(a, Circle) and isinstance(b, Circle):
        return bounce(circle_circle(a, b), restitution)
    elif isinstance(a, Polygon) and isinstance(b, Polygon):
        return bounce(polygon_polygon(a, b), restitution)
    elif isinstance(a, Circle) and isinstance(b, Wall):
        return bounce(circle_wall(circle=a, wall=b), restitution)
    elif isinstance(a, Wall) and isinstance(b, Circle):
        return bounce(circle_wall(circle=b, wall=a), restitution)
    elif isinstance(a, Circle) and isinstance(b, Polygon):
        return bounce(circle_polygon(circle=a, polygon=b), restitution)
    elif isinstance(a, Polygon) and isinstance(b, Circle):
        return bounce(circle_polygon(circle=b, polygon=a), restitution)
    elif isinstance(a, Polygon) and isinstance(b, Wall):
        return bounce(polygon_wall(polygon=a, wall=b), restitution)
    elif isinstance(a, Wall) and isinstance(b, Polygon):
        return bounce(polygon_wall(polygon=b, wall=a), restitution)

    return 0
