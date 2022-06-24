from random import uniform

import pygame

from Objects.Polygon import Polygon
from Vec2 import Vec2

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


def make_triangle():
    return Polygon(offsets=[Vec2(uniform(100, 700), uniform(100, 500)), Vec2(uniform(100, 700), uniform(100, 500)),
                            Vec2(uniform(100, 700), uniform(100, 500))], color=RED, width=1, pos=Vec2())


def main():
    pygame.init()
    screen = pygame.display.set_mode([800, 600])

    radius = 50  # circle radius

    # Main Loop
    running = True
    frame_rate = 60

    triangle = make_triangle()

    clock = pygame.time.Clock()
    while running:
        # event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                triangle = make_triangle()

        # mouse position
        pos = Vec2(pygame.mouse.get_pos())

        # overlap detection
        overlap = False
        distance = float("inf")
        normal = Vec2(1, 0)
        point_of_overlap = Vec2(0, 0)

        for i in range(len(triangle.points)):
            n = triangle.normals[i]
            d = (triangle.points[i] - pos) @ n + radius
            if d < distance:
                distance = d
                normal = n
                point_of_overlap = pos + (-n * radius)

        if distance > 0:
            overlap = True
        ''' (1) Check if circle overlaps the triangle '''

        # fill screen background
        if overlap:
            screen.fill(YELLOW)  # Background yellow if inside
        else:
            screen.fill(WHITE)  # Background white if not inside

        # draw shapes
        triangle.draw(screen)
        pygame.draw.circle(screen, BLUE, pos, radius, 1)

        # draw circle and line, if overlapping
        if overlap:
            ''' (2) Draw a small circle at the point of maximum overlap.'''
            pygame.draw.circle(screen, BLACK, point_of_overlap.int(), 5)
            ''' (3) Draw a black line from the point of maximum overlap to the nearest side.'''
            pygame.draw.line(screen, BLACK, point_of_overlap.int(), point_of_overlap + normal * distance)

        # update display
        pygame.display.update()
        clock.tick(frame_rate)

    pygame.quit()


if __name__ == "__main__":
    try:
        main()
    finally:
        pygame.quit()
        raise
