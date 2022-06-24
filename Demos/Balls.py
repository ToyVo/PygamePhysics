import random
from typing import Tuple, List

import pygame

from Objects.Circle import Circle
from Vec2 import Vec2


class Ball(Circle):
    def __init__(self, clickable: bool = False, **kwargs):
        self.clickable = clickable
        super().__init__(**kwargs)


def explode(objects, ball: Ball) -> None:
    objects.append(Ball(radius=ball.radius // 2, color=ball.color, mass=ball.mass / 2, pos=ball.pos,
                        vel=Vec2(ball.vel.x, ball.vel.y), clickable=False))
    objects.append(Ball(radius=ball.radius // 2, color=ball.color, mass=ball.mass / 2, pos=ball.pos,
                        vel=Vec2(-ball.vel.x, ball.vel.y), clickable=False))
    objects.remove(ball)


def gravity(obj) -> Vec2:
    g = Vec2(0, 9.8)
    return obj.mass * g


def new_ball() -> Ball:
    return Ball(radius=100, color=[random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)],
                pos=Vec2(random.randint(100, 700), 600), mass=1,
                vel=(random.randint(-500, 500), random.randint(-1000, -100)))


def main() -> None:
    score: int = 0
    bg_color: Tuple[int, int, int] = 0, 0, 0
    screen_size: Tuple[int, int] = 1200, 800

    pygame.init()
    screen = pygame.display.set_mode(size=screen_size)
    screen.fill(bg_color)

    # set up objects
    objects: List[Ball] = [new_ball()]

    # game loop
    running: bool = True
    paused: bool = False
    disable_gravity: bool = False
    laser_mode: bool = False
    clock = pygame.time.Clock()
    fps: float = 60
    dt: float = 1 / fps
    black: Tuple[int, int, int] = 0, 0, 0
    font = pygame.font.Font("freesansbold.ttf", 16)

    while running:

        # update objects
        if not paused:
            for o in objects:
                if not disable_gravity:
                    o.add_force(gravity(o))
            for o in objects:
                o.update(dt)
                if o.pos.y > 600 + o.radius:
                    objects.remove(o)
                    if score > 0 and o.clickable:
                        score -= 1
                if o.pos.y < o.radius:
                    o.vel.y = -o.vel.y
                if o.pos.x > 800 - o.radius or o.pos.x < o.radius:
                    o.vel.x = -o.vel.x

        # redraw screen
        screen.fill(bg_color)
        screen.blit(font.render("Score: " + str(score), True, black), [10, 10])
        if paused:
            screen.blit(font.render("paused", True, black), [10, 25])
        if disable_gravity:
            screen.blit(font.render("Gravity Disabled", True, black), [10, 40])
        if laser_mode:
            screen.blit(font.render("laser mode", True, black), [10, 55])
        for o in objects:
            o.draw(screen)

        # spawn more balls if empty
        if not objects:
            for x in range(random.randint(1, 3)):
                objects.append(new_ball())

        pygame.display.flip()
        clock.tick(fps)

        # States
        mouse = pygame.mouse.get_pressed()
        if mouse[2] == 1:
            laser_mode = True
            for o in objects:
                if o.clickable and (o.pos - Vec2(pygame.mouse.get_pos())).mag2() < o.radius ** 2:
                    explode(objects, o)
                    score += .5
        else:
            laser_mode = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_b] == 1:
            disable_gravity = True
        else:
            disable_gravity = False

        # Events
        for e in pygame.event.get():
            if e.type == pygame.QUIT or e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:  # user clicked close
                running = False
                pygame.quit()
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                for o in objects:
                    if o.clickable and (o.pos - Vec2(pygame.mouse.get_pos())).mag2() < o.radius ** 2:
                        explode(objects, o)
                        score += 1
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    paused = not paused

    pygame.quit()


# safe start
if __name__ == "__main__":
    try:
        main()
    finally:
        pygame.quit()
