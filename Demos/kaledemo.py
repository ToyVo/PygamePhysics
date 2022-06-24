from typing import Tuple, List

import pygame

from Objects.Circle import Circle
from Objects.Particle import Particle
from Vec2 import Vec2


def main() -> None:
    bg_color: Tuple[int, int, int] = 0, 0, 0
    screen_size: Tuple[int, int] = 1200, 800

    pygame.init()
    screen = pygame.display.set_mode(size=screen_size)
    screen.fill(bg_color)

    # set up objects
    objects: List[Particle] = [Circle(radius=100, pos=Vec2(400, 300), mass=1)]

    # game loop
    running: bool = True
    clock = pygame.time.Clock()
    fps: float = 60
    dt: float = 1 / fps
    while running:
        for o in objects:
            o.update(dt)

        screen.fill(bg_color)
        for o in objects:
            o.draw(screen)

        pygame.display.flip()

        dt = clock.tick(fps) / 1000

        for e in pygame.event.get():
            if e.type == pygame.QUIT:  # user clicked close
                running = False

    pygame.quit()


# safe start
if __name__ == "__main__":
    try:
        main()
    finally:
        pygame.quit()
