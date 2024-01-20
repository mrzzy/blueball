import pygame
from enum import Enum, auto

screen_width = 1280
screen_height = 720
clock = pygame.time.Clock()
running = True
fps = 60
grav = 300
movement = 300
IDLE_SPRITES_PATH = [
    'game/assets/monk/idle/idle_1.png',
    'game/assets/monk/idle/idle_2.png',
    'game/assets/monk/idle/idle_3.png',
    'game/assets/monk/idle/idle_4.png',
    'game/assets/monk/idle/idle_5.png',
    'game/assets/monk/idle/idle_6.png',
]

RUN_SPRITES_PATH = [
    'assets/monk/run/run_1.png',
    'assets/monk/run/run_2.png',
    'assets/monk/run/run_3.png',
    'assets/monk/run/run_4.png',
    'assets/monk/run/run_5.png',
    'assets/monk/run/run_6.png',
    'assets/monk/run/run_7.png',
    'assets/monk/run/run_8.png',
]

JUMP_UP_SPRITES_PATH = [
    'assets/monk/j_up/j_up_1.png',
    'assets/monk/j_up/j_up_2.png',
    'assets/monk/j_up/j_up_3.png',
]

JUMP_DOWN_SPRITES_PATH = [
    'assets/monk/j_down/j_down_1.png',
    'assets/monk/j_down/j_down_2.png',
    'assets/monk/j_down/j_down_3.png',
]

KICK_SPRITES_PATH = [
    'assets/monk/air_atk/air_atk_1.png',
    'assets/monk/air_atk/air_atk_2.png',
    'assets/monk/air_atk/air_atk_3.png',
    'assets/monk/air_atk/air_atk_4.png',
    'assets/monk/air_atk/air_atk_5.png',
    'assets/monk/air_atk/air_atk_6.png',
    'assets/monk/air_atk/air_atk_7.png',
]



class KeyStroke(Enum):
    MoveLeft = auto()
    MoveRight = auto()
    Jump = auto()
    Kick = auto()

class Sprite:
    def __init__(self, image_list, end_frame):
        super().__init__()
        self.image_list = []
        self.frame = 0
        self.end_frame = end_frame
        for i in range(0, len(image_list)):
            image = pygame.image.load(image_list[i])
            self.image_list.append(image)

class Character:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.sprite = Sprite(IDLE_SPRITES_PATH, 5)


class Ball:
    def __init__(self):
        self.pos = pygame.Vector2(screen_width / 2, screen_height / 2)
        self.vel = pygame.Vector2(0, 0)
        self.size = 40


class State:
    def __init__(self):
        self.dt = 0
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.player = Character(screen_width / 3, screen_height / 3)
        self.enemy = Character(2 * (screen_width / 3), 2 * (screen_height / 3))
        self.ball = Ball()


def eval(previous_state: State, keystrokes: [KeyStroke]) -> State:
    state = previous_state

    # Some gravity
    state.player.pos.y += grav * state.dt
    state.enemy.pos.y += grav * state.dt
    state.ball.pos.y += grav * state.dt

    # Don't go off screen
    if state.player.pos.y >= screen_height - 128:
        state.player.pos.y = screen_height - 128
    if state.enemy.pos.y >= screen_height - 128:
        state.enemy.pos.y = screen_height - 128
    if state.ball.pos.y >= screen_height - state.ball.size:
        state.ball.pos.y = screen_height - state.ball.size

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        state.player.pos.y -= movement * state.dt
    if keys[pygame.K_s]:
        state.player.pos.y += movement * state.dt
    if keys[pygame.K_a]:
        state.player.pos.x -= movement * state.dt
    if keys[pygame.K_d]:
        state.player.pos.x += movement * state.dt

    # Update ball position based on velocity
    state.ball.pos += state.ball.vel

    # limits FPS to 60
    state.dt = clock.tick(fps) / 1000
    return state
