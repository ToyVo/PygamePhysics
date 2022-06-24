from typing import Tuple, List

import pygame

from Contact.Contact import handle_contact
from Forces.Bond import Bond
from Forces.Gravity import Gravity
from Forces.PairForce import PairForce
from Forces.SingleForce import SingleForce
from Objects.Circle import Circle
from Objects.Particle import Particle
from Vec2 import Vec2


def main() -> None:
    bg_color: Tuple[int, int, int] = 0, 0, 0
    screen_size: Tuple[int, int] = 1200, 800

    pygame.init()
    screen = pygame.display.set_mode(size=screen_size)
    screen.fill(bg_color)

    objects: List[Particle] = [Circle(radius=100, color=(255, 0, 0), pos=Vec2(100, 300), mass=1, vel=Vec2(0, 0)),
        Circle(radius=100, color=(0, 255, 0), pos=Vec2(300, 300), mass=1, vel=Vec2(0, 0)),
        Circle(radius=100, color=(0, 0, 255), pos=Vec2(500, 300), mass=1, vel=Vec2(0, 0)),
        Circle(radius=100, color=(255, 255, 255), pos=Vec2(700, 300), mass=1, vel=Vec2(0, 0))]

    forces: List[SingleForce or PairForce or Bond] = []
    gravity: Gravity = Gravity(objects, Vec2(0, 10))
    forces.append(gravity)

    # Game loop
    running: bool = True
    fps: float = 60
    dt: float = 1 / fps
    clock = pygame.time.Clock()
    while running:
        # Add force and update objects
        for o in objects:
            o.clear_force()
        for f in forces:
            f.apply()
        for o in objects:
            o.update(dt)

        # Redraw
        screen.fill(bg_color)
        for o in objects:
            o.draw(screen)

        # Show what we have drawn
        pygame.display.flip()
        clock.tick(fps)

        handle_contact(objects)

        # Event Loop
        for e in pygame.event.get():
            if e.type == pygame.QUIT or e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                running = False
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                objects.append(Circle(radius=100, pos=Vec2(e.pos), mass=1))

    # Shut down pygame
    pygame.quit()


if __name__ == "__main__":
    try:
        main()
    finally:
        pygame.quit()
