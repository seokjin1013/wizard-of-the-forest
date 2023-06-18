import pygame
import ww
from bullet import Bullet

class Player(pygame.sprite.Sprite):
	def __init__(self, pos, health):
		super().__init__()
		self.health = health
		self.image = ww.Images.player
		self.rect = self.image.get_rect(center=pos)
		self.direction = pygame.math.Vector2()
		self.speed = 5
		self.attack_time = 0
		self.attack_delay = 5

	def input(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_w]:
			self.direction.y = -1
		elif keys[pygame.K_s]:
			self.direction.y = 1
		else:
			self.direction.y = 0

		if keys[pygame.K_d]:
			self.direction.x = 1
		elif keys[pygame.K_a]:
			self.direction.x = -1
		else:
			self.direction.x = 0
			
		if pygame.mouse.get_pressed()[0] and self.attack_time == 0:
			ww.group.add(Bullet(self.rect.center, 20))
			self.attack_time = self.attack_delay

	def update(self):
		self.input()
		self.rect.center += self.direction * self.speed
		self.attack_time = max(self.attack_time - 1, 0)
    		