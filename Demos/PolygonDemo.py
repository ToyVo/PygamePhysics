import random
from typing import Tuple, List

import pygame

from Contact.Contact import handle_contact, draw_overlap
from Forces.Bond import Bond
from Forces.PairForce import PairForce
from Forces.SingleForce import SingleForce
from Objects.Particle import Particle
from Objects.Polygon import Polygon
from Vec2 import Vec2


def main() -> None:
    bg_color: Tuple[int, int, int] = (255, 255, 255)
    screen_size: Tuple[int, int] = (1200, 800)

    pygame.init()
    screen = pygame.display.set_mode(size=screen_size)
    screen.fill(bg_color)

    poly1 = Polygon(pos=Vec2(600, 400), color=(0, 0, 255), draw_normals=True,
                    offsets=[Vec2(100, 100), Vec2(100, -100), Vec2(-100, 100)], mass=100)
    poly2 = Polygon(pos=pygame.mouse.get_pos(), color=(255, 0, 0), draw_normals=True,
                    offsets=[Vec2(100, 100), Vec2(100, -100), Vec2(-100, 100)])

    objects: List[Particle] = [poly1, poly2]

    forces: List[SingleForce or PairForce or Bond] = []

    # Game loop
    running = True
    fps = 60
    dt = 1 / fps
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

        draw_overlap(screen, poly1, poly2)
        for o in objects:
            o.draw(screen)

        # Show what we have drawn
        pygame.display.flip()
        clock.tick(fps)

        poly2.pos = Vec2(pygame.mouse.get_pos())

        # Event Loop
        for e in pygame.event.get():
            if e.type == pygame.QUIT or e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                running = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    handle_contact(objects)
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    random_x = random.randint(100, 1000)
                    random_y = random.randint(100, 600)
                    offset_x1 = random.randint(0, 300)
                    offset_x2 = random.randint(0, 300)
                    offset_x3 = random.randint(0, 300)
                    offset_y1 = random.randint(0, 300)
                    offset_y2 = random.randint(0, 300)
                    offset_y3 = random.randint(0, 300)
                    poly1.pos = Vec2(random_x, random_y)
                    poly1.offsets = [Vec2(offset_x1, offset_y1), Vec2(offset_x2, offset_y2), Vec2(offset_x3, offset_y3)]

    # Shut down pygame
    pygame.quit()


if __name__ == "__main__":
    try:
        main()
    finally:
        pygame.quit()
