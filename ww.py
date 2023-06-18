import pygame

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900

pygame.init()

group = pygame.sprite.Group()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Images:
    player = pygame.image.load('assets/player.png').convert_alpha()
    tree = pygame.image.load('assets/tree.png').convert_alpha()
    bullet = pygame.image.load('assets/bullet.png').convert_alpha()
    view = pygame.image.load('assets/ground.png').convert_alpha()