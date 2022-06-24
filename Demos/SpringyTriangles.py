import math
from typing import List

import pygame

import Color
from Forces.Bond import Bond
from Forces.Gravity import Gravity
from Forces.PairForce import PairForce
from Forces.RepulsiveForce import Repulsive
from Forces.SingleForce import SingleForce
from Forces.Spring import Spring
from Objects.Circle import Circle
from Objects.Particle import Particle
from Objects.Wall import Wall
from Vec2 import Vec2


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode(size=(1200, 800))

    t1a = Circle(radius=15, mass=1, color=Color.RED, pos=Vec2(400, 200 - (30 * math.sqrt(3))))
    t1b = Circle(radius=15, mass=1, color=Color.RED, pos=Vec2(370, 200))
    t1c = Circle(radius=15, mass=1, color=Color.RED, pos=Vec2(430, 200))
    t2a = Circle(radius=15, mass=1, color=Color.BLUE, pos=Vec2(800, 200 - (30 * math.sqrt(3))))
    t2b = Circle(radius=15, mass=1, color=Color.BLUE, pos=Vec2(770, 200))
    t2c = Circle(radius=15, mass=1, color=Color.BLUE, pos=Vec2(830, 200))
    t3a = Circle(radius=15, mass=1, color=Color.YELLOW, pos=Vec2(600, 200 - (30 * math.sqrt(3))))
    t3b = Circle(radius=15, mass=1, color=Color.YELLOW, pos=Vec2(570, 200))
    t3c = Circle(radius=15, mass=1, color=Color.YELLOW, pos=Vec2(630, 200))
    w1 = Wall(pos=Vec2(400, 700), color=Color.BLACK, normal=Vec2(1, -2))
    w2 = Wall(pos=Vec2(800, 700), color=Color.BLACK, normal=Vec2(-1, -2))

    objects: List[Particle] = [t1a, t1b, t1c, t2a, t2b, t2c, t3a, t3b, t3c, w1, w2]
    triangle1 = [(t1a, t1b), (t1b, t1c), (t1c, t1a)]
    triangle2 = [(t2a, t2b), (t2b, t2c), (t2c, t2a)]
    triangle3 = [(t3a, t3b), (t3b, t3c), (t3c, t3a)]

    gravity: Gravity = Gravity(objects, Vec2(0, 100))
    repulsive: Repulsive = Repulsive(objects, strength=250, length=15)
    spring1: Spring = Spring(pair_list=triangle1, k=500, length=60, d=0.003)
    spring2: Spring = Spring(pair_list=triangle2, k=500, length=60, d=0.003)
    spring3: Spring = Spring(pair_list=triangle3, k=500, length=60, d=0.003)
    forces: List[SingleForce or PairForce or Bond] = [gravity, repulsive, spring1, spring2, spring3]

    # Game loop
    running: bool = True
    force_field: bool = False
    force_field_radius = 50
    fps: float = 60
    dt: float = 1 / fps
    clock = pygame.time.Clock()
    while running:
        force_field_pos = Vec2(pygame.mouse.get_pos())

        # Add force and update objects
        for o in objects:
            o.clear_force()
        for f in forces:
            f.apply()

        if force_field:
            for o in objects:
                d = o.pos - force_field_pos
                if d.mag2() < force_field_radius ** 2:
                    o.add_force(-d.hat() * 1000)

        for o in objects:
            o.update(dt)

        # Draw
        screen.fill(Color.WHITE)
        if force_field:
            pygame.draw.circle(screen, Color.BLUE, force_field_pos, force_field_radius, 1)
        for o in objects:
            o.draw(screen)
        spring1.draw(screen)
        spring2.draw(screen)
        spring3.draw(screen)

        # Show what we have drawn
        pygame.display.flip()
        clock.tick(fps) / 1000

        # Event Loop
        for e in pygame.event.get():
            if e.type == pygame.QUIT or e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                running = False
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                for o in objects:
                    o.vel = Vec2()
            elif e.type == pygame.MOUSEBUTTONDOWN:
                force_field = True
            elif e.type == pygame.MOUSEBUTTONUP:
                force_field = False

    pygame.quit()


if __name__ == "__main__":
    try:
        main()
    finally:
        pygame.quit()
