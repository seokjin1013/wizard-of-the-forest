import pygame
import ww
import random
import sys
from monster import *
from player import Player
from view import View
from monster_constuctor import MonsterConstuctor

ww.group = pygame.sprite.LayeredUpdates()
ww.player = Player((640,360))
ww.group.add(ww.player)
ww.view = View(target=ww.player)
ww.monster_constructor = MonsterConstuctor()

for i in range(400):
	random_x = random.randint(0,1000)
	random_y = random.randint(0,1000)
	ww.group.add(Tree((random_x, random_y)))

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()

	# ww.monster_constructor.update()
	ww.world.Step(1 / ww.FPS, 1, 1)
	ww.group.update()
	ww.view.update()
	ww.view.draw()
	pygame.display.flip()