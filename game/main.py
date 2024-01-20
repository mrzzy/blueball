# Example file showing a circle moving on screen
import pygame
import constants

# pygame setup
pygame.init()
screen = pygame.display.set_mode(size = (1280, 720), vsync=1)
clock = pygame.time.Clock()
running = True
dt = 0
isJump = False
left = False
right = False

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

class Sprite:
    def __init__(self, image_list, end_frame, x, y):
        super().__init__()

        self.image = image_list
        self.frame = 0
        self.end_frame = end_frame
        self.x = x
        self.y = y
    
    def animate(self):
        screen.blit(self.image[idle_sprite.frame], (self.x, self.y))
        if idle_sprite.frame + 1 > idle_sprite.end_frame:
            idle_sprite.frame = 0
        idle_sprite.frame += 1

    def animate(self, x, y):
        self.x = x
        self.y = y
        screen.blit(self.image[idle_sprite.frame], (self.x, self.y))
        if idle_sprite.frame + 1 > idle_sprite.end_frame:
            idle_sprite.frame = 0
        idle_sprite.frame += 1


idle_sprite = Sprite(constants.IDLE_SPRITES, 5, player_pos.x, player_pos.y)
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")
    idle_sprite.animate(player_pos.x, player_pos.y)
    pygame.draw.rect(screen, "green", (1250, 0, 30, 720))
    pygame.draw.rect(screen, "red", (0, 0, 30, 720))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()