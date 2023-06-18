import pygame
import random
import sys
import ww
from monster import *
from player import Player
from view import View
from monster_constuctor import MonsterConstuctor

ww.player = Player((640,360), 120)
ww.player_group = pygame.sprite.GroupSingle(ww.player)
ww.group.add(ww.player_group)
ww.view = View(target=ww.player, debug=True)
ww.tree_group = pygame.sprite.Group()
ww.monster_constuctor = MonsterConstuctor()

for i in range(20):
	random_x = random.randint(0,1000)
	random_y = random.randint(0,1000)
	ww.tree_group.add(Tree((random_x, random_y)))
ww.group.add(ww.tree_group)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()
	ww.view.step()
	ww.view.draw()
	ww.monster_constuctor.update()
	ww.group.update()
	pygame.display.update()
