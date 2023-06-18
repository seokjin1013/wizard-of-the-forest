import pygame
import ww
import random
import sys
from monster import *
from player import Player
from view import View
from monster_constuctor import MonsterConstuctor
from controller import Controller
from title import Title, TitleButton

# set up for starting game
ww.group = pygame.sprite.LayeredUpdates()
ww.group.add(Title((320, 180)))
def callback():
	ww.phase = ww.PHASE.PLAY
	ww.player = Player((320, 180))
	ww.group.add(ww.player)
	ww.view.target = ww.player
ww.group.add(TitleButton((320, 280), 0, callback))
ww.view = View()
ww.monster_constructor = MonsterConstuctor()
ww.controller = Controller()

for i in range(0):
	random_x = random.randint(0,1000)
	random_y = random.randint(0,100)
	ww.group.add(Tree((random_x, random_y)))

clock = pygame.time.Clock()
clock2 = pygame.time.Clock()
delayed_time = 0

# runtime loop

while True:
	# function key
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()

	delayed_time += clock.tick() - 1000 / ww.FPS

	# loop operation
	if ww.phase == ww.PHASE.PLAY:
		ww.monster_constructor.update()
	ww.controller.update()
	ww.world.Step(1 / ww.FPS, 1, 1)
	ww.group.update()
	ww.view.update()

	# frameskip
	if delayed_time < 0:
		clock2.tick(ww.FPS)
		ww.view.debug_text.append(round(clock.get_fps(), 2))
		ww.view.debug_text.append(round(clock2.get_fps(), 2))
		ww.view.debug_text.append(len(ww.group))
		ww.view.draw()
		pygame.display.flip()

	