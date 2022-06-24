import math
from itertools import combinations
from typing import List

import pygame

import Color
from Contact.Contact import handle_contact
from Contact.circle_circle import circle_circle
from Forces.Friction import Friction
from Objects.Circle import Circle
from Objects.Particle import Particle
from Objects.UniformPolygon import UniformPolygon
from Objects.Wall import Wall
from Vec2 import Vec2

bg_color = 79, 79, 79
screen_size = 1200, 800


class Player(Circle):
    def __init__(self, player: int, health=12, damage=6, **kwargs):
        self.player: int = player
        self.health: float = health
        self.damage: float = damage
        self.dead: bool = False
        super().__init__(**kwargs)


def handle_hit(particle_list: List[Particle], current_player: int):
    for a, b in combinations(particle_list, 2):
        if isinstance(a, Player) and isinstance(b, Player) and a.player != b.player:
            _a, _b, d, n, p = circle_circle(a, b)
            red = None
            blue = None
            if a.color == Color.RED:
                red = a
            else:
                blue = a

            if b.color == Color.RED:
                red = b
            else:
                blue = b

            if d > 0 and red is not None and blue is not None:
                if red.color != Color.WHITE and blue.color != Color.WHITE:
                    if current_player == 1:
                        blue.health -= red.damage
                    elif current_player == 2:
                        red.health -= blue.damage


def handle_cue_hit(current_player, mouse_down_pos: Vec2, mouse_up_pos: Vec2, objects):
    if mouse_down_pos != mouse_up_pos:
        # find equation of line
        m = (mouse_up_pos.y - mouse_down_pos.y) / (mouse_up_pos.x - mouse_down_pos.x)
        b = -mouse_down_pos.x * m + mouse_down_pos.y
        direction_start_end = (mouse_up_pos - mouse_down_pos).normalize()
        direction_end_start = (mouse_down_pos - mouse_up_pos).normalize()
        point_of_contact: Vec2 = Vec2()
        # noinspection PyTypeChecker
        hit_object: Circle = None

        for o in objects:
            if isinstance(o, Player) and o.player is not None and o.player == current_player:
                a = o.pos.x
                c = o.pos.y
                r = o.radius

                qf1 = 2 * (m * c + a - m * b)
                qf2 = 8 * (m * c * a + b * c - m * b * a) + 4 * (
                        r ** 2 - b ** 2 - c ** 2 - m ** 2 * a ** 2 + m ** 2 * r ** 2)
                qf3 = 2 + 2 * m ** 2

                try:
                    x1 = (qf1 + math.sqrt(qf2)) / qf3
                    x2 = (qf1 - math.sqrt(qf2)) / qf3

                    p1 = Vec2(x1, m * x1 + b)
                    p2 = Vec2(x2, m * x2 + b)

                    if (p1 - mouse_down_pos).mag2() < (p2 - mouse_down_pos).mag2():
                        p = p1
                    else:
                        p = p2

                    if (p - mouse_down_pos).normalize() @ direction_start_end > 0 and (
                            p - mouse_up_pos).normalize() @ direction_end_start > 0:
                        if point_of_contact is None or (p - mouse_down_pos).mag2() < (
                                point_of_contact - mouse_down_pos).mag2():
                            point_of_contact = p
                            hit_object = o

                except ValueError:
                    pass

        if hit_object is not None and point_of_contact is not None and hit_object.radius ** 2 - 1 <= (
                point_of_contact - hit_object.pos).mag2() <= hit_object.radius ** 2 + 1:
            hit_object.add_impulse((mouse_up_pos - mouse_down_pos), point_of_contact)
            return point_of_contact
        else:
            return Vec2()


def switch_player(current_player):
    if current_player == 1:
        return 2
    elif current_player == 2:
        return 1


def switch_turn(current_player):
    if current_player == 2:
        return "Blue's Turn"
    elif current_player == 1:
        return "Red's Turn"
    else:
        return "Game Ended"


def main():
    pygame.init()
    screen = pygame.display.set_mode(size=screen_size)
    screen.fill(bg_color)

    momi = (2 / 5) * 25 ** 2

    objects = [Player(radius=25, pos=Vec2(400, 100), mass=1, color=(255, 0, 0), player=1, momi=momi),
               Player(radius=25, pos=Vec2(400, 300), mass=1, color=(255, 0, 0), player=1, momi=momi),
               Player(radius=25, pos=Vec2(400, 500), mass=1, color=(255, 0, 0), player=1, momi=momi),
               Player(radius=25, pos=Vec2(400, 700), mass=1, color=(255, 0, 0), player=1, momi=momi),
               Player(radius=25, pos=Vec2(800, 100), mass=1, color=(0, 0, 255), player=2, momi=momi),
               Player(radius=25, pos=Vec2(800, 300), mass=1, color=(0, 0, 255), player=2, momi=momi),
               Player(radius=25, pos=Vec2(800, 500), mass=1, color=(0, 0, 255), player=2, momi=momi),
               Player(radius=25, pos=Vec2(800, 700), mass=1, color=(0, 0, 255), player=2, momi=momi),
               Wall(pos=Vec2(600, 20), normal=Vec2(0, 1), length=580, color=(0, 0, 0)),
               Wall(pos=Vec2(600, 780), normal=Vec2(0, -1), length=580, color=(0, 0, 0)),
               Wall(pos=Vec2(20, 400), normal=Vec2(1, 0), length=380, color=(0, 0, 0)),
               Wall(pos=Vec2(1180, 400), normal=Vec2(-1, 0), length=380, color=(0, 0, 0)),
               Circle(radius=25, pos=Vec2(700, 400), color=(255, 255, 255)),
               Circle(radius=25, pos=Vec2(500, 400), color=(255, 255, 255)),
               Circle(radius=25, pos=Vec2(600, 300), color=(255, 255, 255)),
               Circle(radius=25, pos=Vec2(600, 500), color=(255, 255, 255)),
               UniformPolygon(pos=Vec2(150, 150), offsets=[Vec2(50, 50), Vec2(0, 50), Vec2(50, 0)], density=0.025,
                              color=Color.WHITE, infinite_mass=True),
               UniformPolygon(pos=Vec2(1050, 150), offsets=[Vec2(0, 50), Vec2(-25, 0), Vec2(25, 0)], density=0.025,
                              color=Color.WHITE, infinite_mass=True),
               UniformPolygon(pos=Vec2(150, 650), offsets=[Vec2(60, 20), Vec2(0, 90), Vec2(20, 0)], density=0.025,
                              color=Color.WHITE, infinite_mass=True),
               UniformPolygon(pos=Vec2(1050, 650), offsets=[Vec2(80, 10), Vec2(60, 20), Vec2(20, -10)], density=0.025,
                              color=Color.WHITE, infinite_mass=True)]

    forces = [Friction(objects, d=1)]
    current_player = 1
    turn = "Red's Turn"

    # Game loop
    running = True
    fps = 60
    dt = 1 / fps
    clock = pygame.time.Clock()
    mouse_down_pos = Vec2()
    mouse_up_pos = Vec2()
    turn_taken = False
    font = pygame.font.Font("freesansbold.ttf", 36)
    cue_hit_pos = Vec2()

    while running:

        for f in forces:
            f.apply()

        # Event Loop
        for e in pygame.event.get():
            if e.type == pygame.QUIT or e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                running = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    if not turn_taken:
                        mouse_down_pos = Vec2(pygame.mouse.get_pos())
                        mouse_up_pos = Vec2()
                        cue_hit_pos = Vec2()

            elif e.type == pygame.MOUSEBUTTONUP:
                if e.button == 1:
                    if not turn_taken:
                        mouse_up_pos = Vec2(pygame.mouse.get_pos())
                        cue_hit_pos = handle_cue_hit(current_player, mouse_down_pos, mouse_up_pos, objects)
                    turn_taken = True

        is_everyone_still = True
        for o in objects:
            o.update(dt)
            if o.vel.mag2() > 5:
                is_everyone_still = False

            if isinstance(o, Player):
                if o.health <= 0 and not o.dead and o.radius == 25:
                    if o.player == 1:
                        temp_pos_x = o.pos.x + 25
                        temp_pos_y = o.pos.y + 25
                        o.dead = True
                        objects.append(
                            Player(radius=15, pos=Vec2(temp_pos_x, temp_pos_y), mass=1, color=(255, 0, 0), player=1,
                                   health=100, damage=4, vel=(15, 15)))
                        objects.append(
                            Player(radius=15, pos=Vec2(o.pos.x, o.pos.y), mass=1, color=(255, 0, 0), player=1,
                                   health=100, damage=4, vel=(15, 15)))
                        objects.remove(o)
                    if o.player == 2:
                        temp_pos_x = o.pos.x + 25
                        temp_pos_y = o.pos.y + 25
                        o.dead = True
                        objects.append(
                            Player(radius=15, pos=Vec2(temp_pos_x, temp_pos_y), mass=0.5, color=(0, 0, 255), player=2,
                                   health=100, damage=4, vel=(15, 15)))
                        objects.append(
                            Player(radius=15, pos=Vec2(o.pos.x, o.pos.y), mass=0.5, color=(0, 0, 255), player=2,
                                   health=100, damage=4, vel=(15, 15)))
                        objects.remove(o)
                elif o.health <= 0 and o.radius == 15:
                    objects.remove(o)

        # deals with turns
        if is_everyone_still and turn_taken:
            for obj in objects:
                obj.vel = Vec2()

            if turn_taken:
                current_player = switch_player(current_player)
                turn = switch_turn(current_player)
                turn_taken = False

        # Contact
        handle_hit(objects, current_player)
        handle_contact(objects)

        # Draw
        screen.fill(bg_color)
        screen.blit(font.render(str(turn), True, (0, 0, 0)), [500, 50])
        red_count = 0
        blue_count = 0
        for o in objects:
            if o.color == Color.RED:
                red_count += 1
                if o.health > 12:
                    o.health = 3
            elif o.color == Color.BLUE:
                blue_count += 1
                if o.health > 12:
                    o.health = 3
        if red_count == 0:
            screen.blit(font.render("Blue Won!", True, (0, 0, 255)), [525, 600])
            current_player = 3
        elif blue_count == 0:
            screen.blit(font.render("Red Won!", True, (255, 0, 0)), [525, 600])
            current_player = 3

        for o in objects:
            o.draw(screen)
            if o.color != Color.WHITE and isinstance(o, Circle):
                x = o.pos.x - (o.radius / 1.5)
                y = o.pos.y - (o.radius / 1.5)
                screen.blit(font.render(str(o.health), True, (0, 0, 0)), [x, y])

        if mouse_down_pos != Vec2():
            if mouse_up_pos == Vec2():
                pygame.draw.line(screen, Color.BLACK, mouse_down_pos, pygame.mouse.get_pos())
            else:
                pygame.draw.line(screen, Color.BLACK, mouse_down_pos, mouse_up_pos)
        if cue_hit_pos is not None and cue_hit_pos != Vec2():
            pygame.draw.circle(screen, Color.BLACK, cue_hit_pos.int(), 5)

        # Show what we have drawn
        pygame.display.flip()
        clock.tick(fps) / 1000

        for o in objects:
            o.clear_force()

    # Shut down pygame
    pygame.quit()


if __name__ == "__main__":
    try:
        main()
    finally:
        pygame.quit()
