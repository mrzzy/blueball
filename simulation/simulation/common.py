import pygame
from enum import Enum, auto

screen_width = 1280
screen_height = 720
clock = pygame.time.Clock()
running = True
fps = 60
grav = 100
movement = 300
scale = 3
jump_max = 10
jump_count = 0
magic_number = 17

sprite_width = 288
sprite_height = 128

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
    JumpingUp = auto()
    JumpingDown = auto()


class Character:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.current_state = CharacterState.Idle
        self.idle_sprite = Sprite(IDLE_SPRITES_PATH, 5)
        self.running_sprite = Sprite(RUN_SPRITES_PATH, 7)
        self.kicking_sprite = Sprite(KICK_SPRITES_PATH, 6)
        self.jumping_up_sprite = Sprite(JUMP_UP_SPRITES_PATH, 2)
        self.jumping_down_sprite = Sprite(JUMP_DOWN_SPRITES_PATH, 2)
        self.next_frame_time = 0
        self.is_jumping = False
        self.jump_count = 10
        self.direction = 0  # 0 is to the left, 1 is to the right

    def get_sprite(self) -> Sprite:
        if self.current_state == CharacterState.Idle:
            return self.idle_sprite
        if self.current_state == CharacterState.Running:
            return self.running_sprite
        if self.current_state == CharacterState.JumpingUp:
            return self.jumping_up_sprite
        if self.current_state == CharacterState.JumpingDown:
            return self.jumping_down_sprite
        return self.kicking_sprite

    def draw(self, state, inter_frame_delay, position, special_flags=0):
        time_now = pygame.time.get_ticks()
        if time_now > self.next_frame_time:
            inter_frame_delay = 140
            self.next_frame_time = time_now + inter_frame_delay
            if self.get_sprite().frame + 1 > self.get_sprite().end_frame:
                # Set current frame to 0
                self.get_sprite().frame = 0
                if self.current_state != CharacterState.Idle:
                    self.current_state = CharacterState.Idle
                # Set the next state's frame to 0 as well
                self.get_sprite().frame = 0
            self.get_sprite().frame += 1

        center_sprite = (
            position.x
            - (self.get_sprite().image_list[self.get_sprite().frame].get_width() / 2),
            position.y
            - (
                (self.get_sprite().image_list[0].get_height() / 2)
                + self.get_sprite().image_list[self.get_sprite().frame].get_height()
                - 17
            ),
        )
        state.screen.blit(
            self.get_sprite().image_list[self.get_sprite().frame]
            if self.direction
            else pygame.transform.flip(
                self.get_sprite().image_list[self.get_sprite().frame],
                True,
                False,
            ),
            center_sprite,
            special_flags=special_flags,
        )


class Background:
    def __init__(self):
        self.sprite = Sprite(BACKGROUND_SPRITES_PATH, 5)

    def draw(self, state, pos=(0, 0)):
        for i in range(len(self.sprite.image_list)):
            state.screen.blit(self.sprite.image_list[i], pos)


class Ball:
    def __init__(self):
        self.pos = pygame.Vector2(screen_width / 2, screen_height / 2)
        self.vel = pygame.Vector2(0, 0)
        self.size = 40


class State:
    def __init__(self):
        self.dt = 0
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.player = Character(screen_width / 3, screen_height - 100)
        self.enemy = Character(2 * (screen_width / 3), screen_height - 100)
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

    # When kicking, if the ball is nearby, move the ball
    if state.player.current_state == CharacterState.Kicking:
        if state.player.get_sprite().frame in [0, 1]:
            if state.player.direction == 1:  # To the right
                right_x = (
                    state.player.pos.x
                    + (sprite_width * scale)
                    - ((sprite_width / 2) - 5) * scale
                )
                right_y = (
                    state.player.pos.y
                    + (sprite_width * scale)
                    - ((sprite_width / 2) - 5) * scale
                )
                if (
                    state.ball.pos.x >= right_x
                    and state.ball.pos.x <= right_x + 50
                    and state.ball.pos.y <= right_y
                ):
                    state.ball.vel = (25, 0)

    # Update ball position based on velocity
    state.ball.pos += state.ball.vel

    player_moved = False
    enemy_moved = False
    for keystroke in userinput.keystrokes:
        # Whlie it is in the air
        if state.player.current_state == CharacterState.JumpingUp:
            player_moved = True
            state.player.pos.y -= movement * state.dt * 2
            if keystroke == KeyStroke.P_MoveLeft:
                state.player.pos.x -= movement * state.dt
            elif keystroke == KeyStroke.P_MoveRight:
                state.player.pos.x += movement * state.dt

            if state.player.get_sprite().frame == state.player.get_sprite().end_frame:
                state.player.current_state = CharacterState.JumpingDown
        elif state.player.current_state == CharacterState.JumpingDown:
            player_moved = True
            state.player.pos.y -= movement * state.dt * 2
            if state.player.pos.y == 0:
                state.player.current_state = CharacterState.Idle

        # Not allowed to move when its kicking
        elif (
            state.player.current_state != CharacterState.Kicking
            or state.player.current_state != CharacterState.JumpingDown
            or state.player.current_state != CharacterState.JumpingUp
        ):
            if keystroke == KeyStroke.P_MoveLeft:
                player_moved = True
                state.player.current_state = CharacterState.Running
                state.player.direction = 0
                state.player.pos.x -= movement * state.dt
            if keystroke == KeyStroke.P_MoveRight:
                player_moved = True
                state.player.current_state = CharacterState.Running
                state.player.direction = 1
                state.player.pos.x += movement * state.dt
            if keystroke == KeyStroke.P_Kick:
                player_moved = True
                state.player.current_state = CharacterState.Kicking
            if keystroke == KeyStroke.P_Jump:
                player_moved = True
                state.player.current_state = CharacterState.JumpingUp

        if state.enemy.current_state != CharacterState.Kicking:
            if keystroke == KeyStroke.E_MoveLeft:
                enemy_moved = True
                state.enemy.current_state = CharacterState.Running
                state.enemy.direction = 0
                state.enemy.pos.x -= movement * state.dt
            if keystroke == KeyStroke.E_MoveRight:
                enemy_moved = True
                state.enemy.current_state = CharacterState.Running
                state.enemy.direction = 1
                state.enemy.pos.x += movement * state.dt
            if keystroke == KeyStroke.E_Kick:
                enemy_moved = True
                state.enemy.current_state = CharacterState.Kicking
            if keystroke == KeyStroke.E_Jump:
                enemy_moved = True
                state.enemy.current_state = CharacterState.JumpingUp

    # if state.player.is_jumping:
    #     state.player.pos.y -= jump_count
    #     if jump_count > -jump_max:
    #         jump_count -= 1
    #     else:
    #         state.player.is_jumping = False

    if not player_moved and state.player.current_state == CharacterState.Running:
        state.player.current_state = CharacterState.Idle
        state.player.get_sprite().frame = 0
    if not enemy_moved and state.enemy.current_state == CharacterState.Running:
        state.enemy.current_state = CharacterState.Idle
        state.enemy.get_sprite().frame = 0

    # Don't go off screen
    if state.player.pos.y >= screen_height + magic_number * 2:
        state.player.pos.y = screen_height + magic_number * 2
    if state.enemy.pos.y >= screen_height + magic_number * 2:
        state.enemy.pos.y = screen_height + magic_number * 2
    if state.ball.pos.y >= screen_height - state.ball.size:
        state.ball.pos.y = screen_height - state.ball.size

    # limits FPS to 60
    state.dt = clock.tick(fps) / 1000
    return state
