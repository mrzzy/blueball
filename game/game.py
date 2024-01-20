import pygame
from enum import Enum, auto
from simulation import common

# pygame setup
pygame.init()
running = True


def draw(state: common.State) -> None:
    # fill the screen with a color to wipe away anything from last frame
    state.screen.fill("white")

    # Draw ball
    pygame.draw.circle(state.screen, "blue", state.ball.pos, state.ball.size)

    # Draw player
    pygame.draw.rect(state.screen, "green", pygame.Rect((state.player.pos), (50, 50)))

    # Draw enemy
    pygame.draw.rect(state.screen, "red", pygame.Rect((state.enemy.pos), (50, 50)))

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
