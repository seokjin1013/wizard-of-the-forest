import pygame
import ww
from bullet import Bullet

class Player(pygame.sprite.Sprite):
	def __init__(self, pos, health):
		super().__init__()
		self.health = health
		self.image = ww.Images.player
		self.pos = pos
		self.rect = self.image.get_rect(center=pos)
		self.direction = pygame.math.Vector2()
		self.speed = 5
		self.attack_time = 0
		self.attack_delay = 5

	def input(self):
		keys = pygame.key.get_pressed()

		self.direction.y = keys[pygame.K_s] - keys[pygame.K_w]
		self.direction.x = keys[pygame.K_d] - keys[pygame.K_a]
			
		if pygame.mouse.get_pressed()[0] and self.attack_time == 0:
			ww.group.add(Bullet(self.rect.center, 20))
			self.attack_time = self.attack_delay

	def update(self):
		self.input()
		self.pos += self.direction * self.speed
		self.rect.center = self.pos
		self.attack_time = max(self.attack_time - 1, 0)
    		