import ww
from monster import *
from monster.tree import *
import numpy as np
import pygame


# monster constructor
class MonsterConstuctor:
	def __init__(self):
		super().__init__()
		self.monster_list = ['슬라임', '슬라임', '슬라임', '슬라임', '박쥐',  '박쥐',  '박쥐',  '박쥐',  '박쥐', '늑대', '늑대', '늑대', '스켈레톤', '스켈레톤', '스켈레톤', '스켈레톤']
		self.name2class = {
			'슬라임': Slime,
			'박쥐': Bat,
			'늑대': Wolf,
			'스켈레톤': Skelleton,
		}
		self.pos = ww.view.rect.center
		self.t = 0
		self.dur = 14

	def update(self):
		self.t += 1
		if self.t == self.dur:
			random_number = np.random.choice(len(self.monster_list), 1, replace=False)
			# print(random_number)
			name = self.monster_list[random_number[0]]
			
			# spawn where outside of screen
			sprite = ww.sprites[name]
			r = pygame.Vector2(sprite.images[0].get_bounding_rect().size)
			size = ww.SCREEN_SIZE + r
			line = np.random.uniform(0, (size.x + size.y) * 2)
			pos = -(r - (sprite.x, sprite.y))
			l = min(line, size.x)
			line = max(0, line - size.x)
			pos.x += l
			l = min(line, size.y)
			line = max(0, line - size.y)
			pos.y += l
			l = min(line, size.x)
			line = max(0, line - size.x)
			pos.x -= l
			l = min(line, size.y)
			line = max(0, line - size.y)
			pos.y -= l
			pos += ww.view.rect.topleft
			ww.group.add(self.name2class[name](pos))
			self.t = 0
