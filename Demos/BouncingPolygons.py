from typing import Tuple, List

import pygame

from Contact.Contact import handle_contact
from Forces.Bond import Bond
from Forces.Gravity import Gravity
from Forces.PairForce import PairForce
from Forces.SingleForce import SingleForce
from Objects.Particle import Particle
from Objects.UniformPolygon import UniformPolygon
from Objects.Wall import Wall
from Vec2 import Vec2


def main():
    bg_color: Tuple[int, int, int] = (255, 255, 255)
    screen_size: Tuple[int, int] = (1200, 800)

    pygame.init()
    screen = pygame.display.set_mode(size=screen_size)
    screen.fill(bg_color)

    objects: List[Particle] = [Wall(pos=Vec2(600, 20), normal=Vec2(0, 1), length=580, color=(0, 0, 0)),
                               Wall(pos=Vec2(600, 780), normal=Vec2(0, -1), length=580, color=(0, 0, 0)),
                               Wall(pos=Vec2(20, 400), normal=Vec2(1, 0), length=380, color=(0, 0, 0)),
                               Wall(pos=Vec2(1180, 400), normal=Vec2(-1, 0), length=380, color=(0, 0, 0)),
                               UniformPolygon(pos=Vec2(200, 600),
                                              offsets=[Vec2(0, 0), Vec2(50, 0), Vec2(50, 50), Vec2(0, 50)]),
                               UniformPolygon(pos=Vec2(200, 600), offsets=[Vec2(0, 0), Vec2(50, 0), Vec2(50, 50)]),
                               UniformPolygon(pos=Vec2(200, 600),
                                              offsets=[Vec2(0, 0), Vec2(50, 0), Vec2(50, 50), Vec2(0, 50)]),
                               UniformPolygon(pos=Vec2(200, 600),
                                              offsets=[Vec2(0, 0), Vec2(50, 30), Vec2(50, 50), Vec2(0, 50)]),
                               UniformPolygon(pos=Vec2(200, 600),
                                              offsets=[Vec2(0, 0), Vec2(20, 15), Vec2(40, 30), Vec2(50, 50),
                                                       Vec2(0, 50)]), ]
    gravity = Gravity(objects, Vec2(0, 9.8))
    forces: List[SingleForce or PairForce or Bond] = [gravity]

    # Game loop
    running = True
    fps = 60
    dt = 1 / fps
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

        handle_contact(objects)

        # Redraw
        screen.fill(bg_color)
        for o in objects:
            o.draw(screen)

        # Show what we have drawn
        pygame.display.flip()
        clock.tick(fps) / 1000

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
