import pygame
from enum import Enum, auto
from simulation import common
from typing import List
player = common.Character(100, 100)


def draw(state: common.State) -> None:
    # fill the screen with a color to wipe away anything from last frame
    state.screen.fill("white")


    # Draw ball
    pygame.draw.circle(state.screen, "blue", state.ball.pos, state.ball.size)

    # Draw player
    state.screen.blit(player.sprite.image_list[player.sprite.frame], state.player.pos)
    if player.sprite.frame + 1 > player.sprite.end_frame:
        player.sprite.frame = 0
    player.sprite.frame += 1


    # Draw enemy
    state.screen.blit(player.sprite.image_list[player.sprite.frame], state.enemy.pos)
    if player.sprite.frame + 1 > player.sprite.end_frame:
        player.sprite.frame = 0
    player.sprite.frame += 1

    # flip() the display to put your work on screen
    pygame.display.flip()
    return None


def run(player: bool):
    # pygame setup
    pygame.init()
    running = True
    state = common.State()

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

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
                common.KeyStroke.P_Kick
            )

        draw(state)
        state = common.eval(state, common.UserInput(inputs))

    pygame.quit()
