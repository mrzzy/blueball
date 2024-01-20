import pygame
from enum import Enum, auto
from simulation import common

# pygame setup
pygame.init()
running = True
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


state = common.State()

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw(state)
    state = common.eval(state, [])


pygame.quit()
