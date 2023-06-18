import pygame
import random
import sys
import globals
from monster import *
from player import Player
from view import View

globals.player = Player((640,360), 120)
globals.player_group = pygame.sprite.GroupSingle(globals.player)
globals.group.add(globals.player_group)
globals.view = View(target=globals.player, debug=True)
globals.tree_group = pygame.sprite.Group()

for i in range(20):
	random_x = random.randint(0,1000)
	random_y = random.randint(0,1000)
	globals.tree_group.add(Tree((random_x, random_y)))
globals.group.add(globals.tree_group)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()

	globals.view.step()
	globals.view.draw()
	globals.group.update()
	pygame.display.update()
