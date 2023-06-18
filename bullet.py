import pygame
from instance import Instance
import ww
import math
from monster.tree import Tree

class Bullet(Instance):
	def __init__(self, pos):
		super().__init__(pos)
		self.speed = 80
		self.mhp = 20
		self.hp = self.mhp
		self.vel = pygame.math.Vector2(pygame.mouse.get_pos()) + ww.view.rect.topleft - pos
		self.vel.scale_to_length(self.speed)
		deg = pygame.math.Vector2().angle_to(self.vel)
		self.image = pygame.transform.rotate(self.image, 360 - deg)
		self.attack = 1
		
	def update(self):
		super().update()
		self.body.linearVelocity = self.vel

		for ce in self.body.contacts:
			if isinstance(ce.other.userData, Tree):
				ce.other.userData.hp -= self.attack
				self.hp = 0
				break

		if self.hp:
			self.hp -= 1
		else:
			self.kill()