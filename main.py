
import pygame
import config
from player import Player
from game_manager import GameManager

pygame.init()
pygame.mixer.init()  #　初始化声音

screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
clock = pygame.time.Clock()


game_manager = GameManager(screen, 1)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")
    game_manager.update()
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(config.FPS)  # limits FPS to 60

pygame.quit()