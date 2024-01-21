from collections import deque
from operator import itemgetter
import pygame
from enum import Enum, auto
from simulation import common
from typing import List
from sync import sync
import time

def get_sprite(character: common.Character) -> common.Sprite:
    if character.current_state == common.CharacterState.Idle:
        return character.idle_sprite
    if character.current_state == common.CharacterState.Running:
        return character.running_sprite
    if character.current_state == common.CharacterState.Kicking:
        return character.kicking_sprite
    return None


def draw_fps_counter(state):
    font = pygame.font.SysFont("Arial", 18, bold=True)
    fps = str(int(state.clock.get_fps()))
    fps_font = font.render(fps, 1, pygame.Color("RED"))
    state.screen.blit(fps_font, (50, 0))


def draw(state: common.State) -> None:
    # fill the screen with a color to wipe away anything from last frame
    state.screen.fill("white")
    state.background.draw(state)

    # Draw fps
    draw_fps_counter(state)

    # Draw ball
    pygame.draw.circle(state.screen, "blue", state.ball.pos, state.ball.size)

    # Draw player
    state.player.draw(state, 80, state.player.pos)
    # Draw enemy
    state.enemy.draw(state, 80, state.enemy.pos, pygame.BLEND_RGBA_SUB)

    # flip() the display to put your work on screen
    pygame.display.flip()
    return None


def get_user_input(player) -> common.UserInput:
    inputs: List[common.KeyStroke] = []
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        inputs.append(common.KeyStroke.P_MoveLeft) if player else inputs.append(
            common.KeyStroke.E_MoveLeft
        )
    if keys[pygame.K_RIGHT]:
        inputs.append(common.KeyStroke.P_MoveRight) if player else inputs.append(
            common.KeyStroke.E_MoveRight
        )
    if keys[pygame.K_SPACE]:
        inputs.append(common.KeyStroke.P_Jump) if player else inputs.append(
            common.KeyStroke.E_Jump
        )
    if keys[pygame.K_z]:
        inputs.append(common.KeyStroke.P_Kick) if player else inputs.append(
            common.KeyStroke.E_Kick
        )
    return common.UserInput(inputs)

def server_sync(*args):
    class Promise:
        def is_ready(self):
            return False
    return Promise()

def run(player: bool):
    # pygame setup
    pygame.init()
    
    def get_user_inputs():
        running = True
        state = common.State()
        while running:
            state.clock.tick()
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            yield get_user_input(player)
        
        pygame.quit()
    
    add_timestamp = lambda x: (time.time(), x)

    ity = add_timestamp(common.State())

    xs = get_user_inputs()
    txs = map(add_timestamp, xs)

    def poll_and_merge_inputs_and_states(txs):
        s_txs = deque(maxlen=10)
        for tx in txs:
            s_txs.append(server_sync(tx))
            if s_txs[0].is_ready():
                yield s_txs[0]
                s_txs.popleft()
            yield tx

    tzs = poll_and_merge_inputs_and_states(txs)

    tys = sync.client_step(ity, tzs, common.eval)

    ys = map(itemgetter(1), tys)

    for y in ys:
        draw(y)