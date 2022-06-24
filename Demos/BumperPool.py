import pygame

from Contact.Contact import handle_contact
from Forces.Friction import Friction
from Objects.Circle import Circle
from Objects.Wall import Wall
from Vec2 import Vec2

bg_color = 79, 79, 79
screen_size = 1200, 800


class Player(Circle):
    def __init__(self, player: int, **kwargs):
        self.player = player
        super().__init__(**kwargs)


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


def main():
    pygame.init()
    screen = pygame.display.set_mode(size=screen_size)
    screen.fill(bg_color)

    objects = [Circle(radius=50, pos=Vec2(600, 400), color=(0, 0, 0)),
               Player(radius=25, pos=Vec2(400, 100), mass=1, color=(255, 0, 0), player=1),
               Player(radius=25, pos=Vec2(400, 300), mass=1, color=(255, 0, 0), player=1),
               Player(radius=25, pos=Vec2(400, 500), mass=1, color=(255, 0, 0), player=1),
               Player(radius=25, pos=Vec2(400, 700), mass=1, color=(255, 0, 0), player=1),
               Player(radius=25, pos=Vec2(800, 100), mass=1, color=(0, 0, 255), player=2),
               Player(radius=25, pos=Vec2(800, 300), mass=1, color=(0, 0, 255), player=2),
               Player(radius=25, pos=Vec2(800, 500), mass=1, color=(0, 0, 255), player=2),
               Player(radius=25, pos=Vec2(800, 700), mass=1, color=(0, 0, 255), player=2),
               Wall(pos=Vec2(600, 20), normal=Vec2(0, 1), length=580, color=(0, 0, 0)),
               Wall(pos=Vec2(600, 780), normal=Vec2(0, -1), length=580, color=(0, 0, 0)),
               Wall(pos=Vec2(20, 400), normal=Vec2(1, 0), length=380, color=(0, 0, 0)),
               Wall(pos=Vec2(1180, 400), normal=Vec2(-1, 0), length=380, color=(0, 0, 0)),
               Circle(radius=25, pos=Vec2(150, 150), color=(255, 255, 255)),
               Circle(radius=25, pos=Vec2(1050, 150), color=(255, 255, 255)),
               Circle(radius=25, pos=Vec2(150, 650), color=(255, 255, 255)),
               Circle(radius=25, pos=Vec2(1050, 650), color=(255, 255, 255)),
               Circle(radius=25, pos=Vec2(700, 400), color=(255, 255, 255)),
               Circle(radius=25, pos=Vec2(500, 400), color=(255, 255, 255)),
               Circle(radius=25, pos=Vec2(600, 300), color=(255, 255, 255)),
               Circle(radius=25, pos=Vec2(600, 500), color=(255, 255, 255))]

    forces = [Friction(objects, d=1)]
    current_player = 1
    turn = "Red's Turn"

    # Game loop
    running = True
    fps = 60
    dt = 1 / fps
    clock = pygame.time.Clock()
    active_object = None
    mouse_down_pos = Vec2()
    turn_taken = False
    player1_score = 0
    player2_score = 0
    moving = False
    can_be_moved = True
    another_turn = False
    font = pygame.font.Font("freesansbold.ttf", 36)
    while running:

        for f in forces:
            f.apply()

        # Event Loop
        for e in pygame.event.get():
            if e.type == pygame.QUIT or e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                running = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                for o in objects:
                    if e.button == 1:
                        if isinstance(o, Player) and o.player == current_player and not moving:
                            mouse_down_pos = Vec2(pygame.mouse.get_pos())
                            if (o.pos - mouse_down_pos).mag2() < o.radius ** 2 and can_be_moved:
                                active_object = o
                                moving = True
                                can_be_moved = False

            elif e.type == pygame.MOUSEBUTTONUP:
                for o in objects:
                    if active_object == o and moving:
                        direction = (Vec2(pygame.mouse.get_pos()) - mouse_down_pos)
                        active_object.vel += direction
                        moving = False

        for o in objects:
            o.update(dt)
            if active_object == o:
                if 0 < o.vel.mag2() < 5 and not turn_taken:
                    active_object = None
                    o.vel = Vec2(0, 0)
                    moving = False
                    turn_taken = True
            if isinstance(o, Player):
                if o.pos.y > screen_size[1] + o.radius:
                    objects.remove(o)
                elif 350 < o.pos.y - 25 < 450 and 350 < o.pos.y + 25 < 450 and 550 < o.pos.x + 25 < 650 and 550 < o.pos.x - 25 < 650:
                    if o.player == 1:
                        player1_score += 1
                    elif o.player == 2:
                        player2_score += 1
                    objects.remove(o)
                    moving = False
                    if o.player == current_player:
                        can_be_moved = True
                        another_turn = True

        if turn_taken and not another_turn:
            current_player = switch_player(current_player)
            turn = switch_turn(current_player)
            turn_taken = False
            can_be_moved = True

        if turn_taken and another_turn:
            another_turn = False
            can_be_moved = True

        # Contact
        handle_contact(objects)

        # Draw
        screen.fill(bg_color)
        screen.blit(font.render("Red's Score: " + str(player1_score), True, (0, 0, 0)), [50, 50])
        screen.blit(font.render("Blue's Score: " + str(player2_score), True, (0, 0, 0)), [900, 50])
        screen.blit(font.render(str(turn), True, (0, 0, 0)), [500, 50])

        if player1_score == 4:
            screen.blit(font.render("Red Won!", True, (255, 0, 0)), [525, 600])
            current_player = 3
        elif player2_score == 4:
            screen.blit(font.render("Blue Won!", True, (0, 0, 255)), [525, 600])
            current_player = 3

        for o in objects:
            o.draw(screen)

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
