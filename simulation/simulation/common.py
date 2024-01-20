import pygame
from enum import Enum, auto

screen_width = 1280
screen_height = 720
clock = pygame.time.Clock()
running = True
fps = 60
grav = 300
movement = 300
scale = 3

IDLE_SPRITES_PATH = [
    "game/assets/monk/idle/idle_1.png",
    "game/assets/monk/idle/idle_2.png",
    "game/assets/monk/idle/idle_3.png",
    "game/assets/monk/idle/idle_4.png",
    "game/assets/monk/idle/idle_5.png",
    "game/assets/monk/idle/idle_6.png",
]

RUN_SPRITES_PATH = [
    "game/assets/monk/run/run_1.png",
    "game/assets/monk/run/run_2.png",
    "game/assets/monk/run/run_3.png",
    "game/assets/monk/run/run_4.png",
    "game/assets/monk/run/run_5.png",
    "game/assets/monk/run/run_6.png",
    "game/assets/monk/run/run_7.png",
    "game/assets/monk/run/run_8.png",
]

JUMP_UP_SPRITES_PATH = [
    "game/assets/monk/j_up/j_up_1.png",
    "game/assets/monk/j_up/j_up_2.png",
    "game/assets/monk/j_up/j_up_3.png",
]

JUMP_DOWN_SPRITES_PATH = [
    "game/assets/monk/j_down/j_down_1.png",
    "game/assets/monk/j_down/j_down_2.png",
    "game/assets/monk/j_down/j_down_3.png",
]

KICK_SPRITES_PATH = [
    "game/assets/monk/air_atk/air_atk_1.png",
    "game/assets/monk/air_atk/air_atk_2.png",
    "game/assets/monk/air_atk/air_atk_3.png",
    "game/assets/monk/air_atk/air_atk_4.png",
    "game/assets/monk/air_atk/air_atk_5.png",
    "game/assets/monk/air_atk/air_atk_6.png",
    "game/assets/monk/air_atk/air_atk_7.png",
]

BACKGROUND_SPRITES_PATH = [
    "game/assets/bg/Hills Layer 01.png",
    "game/assets/bg/Hills Layer 02.png",
    "game/assets/bg/Hills Layer 03.png",
    "game/assets/bg/Hills Layer 04.png",
    "game/assets/bg/Hills Layer 05.png",
    "game/assets/bg/Hills Layer 06.png",
]

class KeyStroke(Enum):
    # Player keystrokes
    P_MoveLeft = auto()
    P_MoveRight = auto()
    P_Jump = auto()
    P_Kick = auto()

    # Enemy keystrokes
    E_MoveLeft = auto()
    E_MoveRight = auto()
    E_Jump = auto()
    E_Kick = auto()

class Sprite:
    def __init__(self, image_list, end_frame):
        super().__init__()
        self.image_list = []
        self.frame = 0
        self.end_frame = end_frame
        for i in range(0, len(image_list)):
            image = pygame.image.load(image_list[i]).convert_alpha()
            image = pygame.transform.scale(
                image, (image.get_width() * scale, image.get_height() * scale)
            )
            self.image_list.append(image)


class CharacterState(Enum):
    Idle = auto()
    Running = auto()
    Kicking = auto()


class Character:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.current_state = CharacterState.Idle
        self.idle_sprite = Sprite(IDLE_SPRITES_PATH, 5)
        self.running_sprite = Sprite(RUN_SPRITES_PATH, 7)
        self.kicking_sprite = Sprite(KICK_SPRITES_PATH, 6)
        self.next_frame_time = 0

    def get_sprite(self) -> Sprite:
        if self.current_state == CharacterState.Idle:
            return self.idle_sprite
        if self.current_state == CharacterState.Running:
            return self.running_sprite
        # if self.current_state == CharacterState.Kicking:
        #     return self.kicking_sprite
        return self.kicking_sprite

    def draw(self, state, inter_frame_delay, position, special_flags=0):
        time_now = pygame.time.get_ticks()
        if time_now > self.next_frame_time:
            inter_frame_delay = 80
            self.next_frame_time = time_now + inter_frame_delay
            if self.get_sprite().frame + 1 > self.get_sprite().end_frame:
                self.get_sprite().frame = 0
            self.get_sprite().frame += 1
        state.screen.blit(
            self.get_sprite().image_list[self.get_sprite().frame],
            position,
            special_flags=special_flags,
        )

class Background:
    def __init__(self):
        self.sprite = Sprite(BACKGROUND_SPRITES_PATH, 5)
    
    def draw(self, state, pos=(0, 0)):
        for i in range(len(self.sprite.image_list)):
            state.screen.blit(
                self.sprite.image_list[i].convert_alpha(),
                pos
            )



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
        self.background = Background()
        self.ball = Ball()
        self.clock = pygame.time.Clock()


class UserInput:
    def __init__(self, keystrokes):
        self.keystrokes: [KeyStroke] = keystrokes


def eval(previous_state: State, userinput: UserInput) -> State:
    state = previous_state

    # Some gravity
    state.player.pos.y += grav * state.dt
    state.enemy.pos.y += grav * state.dt
    state.ball.pos.y += grav * state.dt

    # Don't go off screen
    if state.player.pos.y >= screen_height - 128 * scale:
        state.player.pos.y = screen_height - 128 * scale
    if state.enemy.pos.y >= screen_height - 128 * scale:
        state.enemy.pos.y = screen_height - 128 * scale
    if state.ball.pos.y >= screen_height - state.ball.size:
        state.ball.pos.y = screen_height - state.ball.size

    # Update ball position based on velocity
    state.ball.pos += state.ball.vel

    for keystroke in userinput.keystrokes:
        if keystroke == KeyStroke.P_MoveLeft:
            state.player.current_state = CharacterState.Running
            state.player.pos.x -= movement * state.dt
        if keystroke == KeyStroke.P_MoveRight:
            state.player.current_state = CharacterState.Running
            state.player.pos.x += movement * state.dt

        if keystroke == KeyStroke.E_MoveLeft:
            state.enemy.current_state = CharacterState.Running
            state.enemy.pos.x -= movement * state.dt
        if keystroke == KeyStroke.E_MoveRight:
            state.enemy.current_state = CharacterState.Running
            state.enemy.pos.x += movement * state.dt

    # limits FPS to 60
    state.dt = clock.tick(fps) / 1000
    return state
