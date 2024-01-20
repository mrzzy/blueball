import pygame
from enum import Enum, auto

screen_width = 1280
screen_height = 720
clock = pygame.time.Clock()
running = True
fps = 60
grav = 300
movement = 300


class KeyStroke(Enum):
    MoveLeft = auto()
    MoveRight = auto()
    Jump = auto()
    Kick = auto()


class Character:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)


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
    if state.player.pos.y >= screen_height - 50:
        state.player.pos.y = screen_height - 50
    if state.enemy.pos.y >= screen_height - 50:
        state.enemy.pos.y = screen_height - 50
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
