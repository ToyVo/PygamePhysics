import random
from typing import List

import pygame

import Color
from Contact.circle_circle import circle_circle
from Forces.Bond import Bond
from Forces.Gravitation import Gravitation
from Forces.PairForce import PairForce
from Forces.SingleForce import SingleForce
from Objects.Circle import Circle
from Objects.Particle import Particle
from Vec2 import Vec2


class Ship(Circle):
    def __init__(self, thrust: float, **kwargs):
        self.thrust = thrust
        super().__init__(**kwargs)


def randomize(sun, checkpoint, ship):
    checkpoint.radius = random.randint(5, 15)
    checkpoint.mass = random.randint(50, 150)
    checkpoint.pos = Vec2(random.randint(100, 400), random.randint(100, 400))
    neg = random.randint(0, 1)
    if neg == 0:
        neg = -1
    checkpoint.vel = (sun.pos - checkpoint.pos).perp().hat() * random.randint(75, 125) * neg
    ship.thrust = random.randint(75, 100)
    ship.radius = random.randint(5, 15)
    ship.mass = random.randint(1, 10)


def out_of_screen(particle: Particle):
    return particle.pos.x < 0 or particle.pos.x > 1000 or particle.pos.y < 0 or particle.pos.y > 1000


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode(size=(1000, 1000))

    sun = Circle(radius=50, mass=500000, color=Color.YELLOW, pos=Vec2(500, 500))
    checkpoint = Circle(color=Color.RED, pos=Vec2())
    ship = Ship(pos=Vec2(500, 250), color=Color.WHITE, vel=Vec2(100, 0), thrust=100)
    randomize(sun, checkpoint, ship)

    objects: List[Particle] = [sun, checkpoint, ship]

    gravitation = Gravitation(objects)

    forces: List[SingleForce or PairForce or Bond] = [gravitation]

    # Game loop
    game_over: bool = False
    fps: float = 60
    dt: float = 1 / fps
    clock = pygame.time.Clock()
    font = pygame.font.Font("freesansbold.ttf", 20)
    score = 0
    time_taken = 0
    while True:
        if not game_over:
            # Add force and update objects
            for o in objects:
                o.clear_force()
            for f in forces:
                f.apply()

            # States
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                ship.add_force(Vec2(ship.thrust, 0))
            if keys[pygame.K_LEFT]:
                ship.add_force(Vec2(-ship.thrust, 0))
            if keys[pygame.K_UP]:
                ship.add_force(Vec2(0, -ship.thrust))
            if keys[pygame.K_DOWN]:
                ship.add_force(Vec2(0, ship.thrust))

            for o in objects:
                o.update(dt)

            if out_of_screen(checkpoint):
                randomize(sun, checkpoint, ship)

            time_taken += dt

        # Draw
        screen.fill(Color.BLACK)
        for o in objects:
            o.draw(screen)
        screen.blit(font.render("Checkpoints Reached: " + str(score), True, Color.WHITE), [10, 40])
        screen.blit(font.render("Time Taken: " + str('%.1f' % time_taken), True, Color.WHITE), [10, 10])
        if game_over:
            screen.blit(font.render("Game Over, press space to restart", True, Color.WHITE), [10, 970])
        if out_of_screen(ship):
            pygame.draw.line(screen, Color.WHITE, sun.pos.int(), ship.pos.int())

        # Show what we have drawn
        pygame.display.flip()
        clock.tick(fps) / 1000

        # Event Loop
        for e in pygame.event.get():
            if e.type == pygame.QUIT or e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                pygame.quit()
            if game_over and e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                game_over = False
                main()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_r:
                randomize(sun, checkpoint, ship)

        a, b, d, n, p = circle_circle(ship, sun)
        if abs(d) < 2:
            game_over = True
        a, b, d, n, p = circle_circle(sun, checkpoint)
        if abs(d) < 2:
            randomize(sun, checkpoint, ship)
        a, b, d, n, p = circle_circle(ship, checkpoint)
        if abs(d) < ship.radius:
            score += 1
            randomize(sun, checkpoint, ship)
        if score >= 7:
            game_over = True


if __name__ == "__main__":
    try:
        main()
    except pygame.error:
        pass
    finally:
        pygame.quit()
