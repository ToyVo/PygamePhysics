from typing import List, Tuple

import pygame

from Contact.Contact import handle_contact
from Forces.AirDrag import AirDrag
from Forces.Bond import Bond
from Forces.Gravity import Gravity
from Forces.PairForce import PairForce
from Forces.SingleForce import SingleForce
from Forces.Spring import Spring
from Functions import get_random_color
from Objects.Circle import Circle
from Objects.Particle import Particle
from Vec2 import Vec2


def main() -> None:
    bg_color: Tuple[int, int, int] = (0, 0, 0)
    air_bar_color: Tuple[int, int, int] = get_random_color()
    screen_size: Tuple[int, int] = (1200, 800)

    pygame.init()
    screen = pygame.display.set_mode(size=screen_size)
    screen.fill(bg_color)

    objects: List[Circle] = [Circle(radius=50, pos=Vec2(screen_size[0] // 2, 100)),
                             Circle(radius=35, pos=Vec2(screen_size[0] // 2, 200), mass=4),
                             Circle(radius=25, pos=Vec2(screen_size[0] // 2, 300), mass=3),
                             Circle(radius=20, pos=Vec2(screen_size[0] // 2, 400), mass=2),
                             Circle(radius=15, pos=Vec2(screen_size[0] // 2, 500), mass=1)]
    pairs = [(objects[i], objects[i + 1]) for i in range(len(objects) - 1)]

    gravity: Gravity = Gravity(objects, Vec2(0, 1000))
    spring: Spring = Spring(pair_list=pairs, k=500, length=100, d=0.003)
    air_drag: AirDrag = AirDrag(objects, 0.0009)
    forces: List[SingleForce or PairForce or Bond] = [gravity, spring, air_drag]

    # Game loop
    running: bool = True
    fps: float = 60
    dt: float = 1 / fps
    clock = pygame.time.Clock()
    # noinspection PyTypeChecker
    active_object: Particle = None
    while running:
        # Add force and update objects
        for o in objects:
            o.clear_force()
        for f in forces:
            f.apply()
        for o in objects:
            if active_object and active_object == o:
                o.pos = Vec2(pygame.mouse.get_pos())
            else:
                o.update(dt)
                if o.pos.y > screen_size[1] + o.radius:
                    objects.remove(o)
                    for f in forces:
                        f.remove(o)

        handle_contact(objects)

        # Draw
        screen.fill(bg_color)
        for o in objects:
            o.draw(screen)
        spring.draw(screen)
        pygame.draw.rect(screen, air_bar_color, pygame.Rect(screen_size[0] // 2, 10, air_drag.wind.x, 30))

        # Show what we have drawn
        pygame.display.flip()
        clock.tick(fps) / 1000

        # States
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            if air_drag.wind.x < 100:
                air_drag.wind += Vec2(1, 0)
        else:
            if air_drag.wind.x > 0:
                air_drag.wind += Vec2(-1, 0)

        if keys[pygame.K_LEFT]:
            if air_drag.wind.x > -100:
                air_drag.wind += Vec2(-1, 0)
        else:
            if air_drag.wind.x < 0:
                air_drag.wind += Vec2(1, 0)

        # Event Loop
        for e in pygame.event.get():
            if e.type == pygame.QUIT or e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                running = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                for o in objects:
                    if o.in_area(Vec2(pygame.mouse.get_pos())):
                        if e.button == 1:
                            active_object = o
                        elif e.button == 3:
                            objects.remove(o)
                            for f in forces:
                                f.remove(o)
            elif e.type == pygame.MOUSEBUTTONUP:
                if active_object:
                    active_object.vel = Vec2()
                    # noinspection PyTypeChecker
                    active_object = None
    # Shut down pygame
    pygame.quit()


if __name__ == "__main__":
    try:
        main()
    finally:
        pygame.quit()
