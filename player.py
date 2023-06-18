import pygame
from instance import Instance
import ww
from bullet import Bullet

class Player(Instance):
	def __init__(self, pos):
		super().__init__(pos)
		self.speed = 25
		self.mhp = 100
		self.hp = self.mhp
		self.attack_time = 0
		self.attack_delay = 4

	def input(self):
		keys = pygame.key.get_pressed()

		self.direction = pygame.math.Vector2(
			keys[pygame.K_d] - keys[pygame.K_a],
			keys[pygame.K_s] - keys[pygame.K_w]
		)
			
		if pygame.mouse.get_pressed()[0] and self.attack_time == 0:
			ww.group.add(Bullet(self.pos))
			self.attack_time = self.attack_delay

	def update(self):
		super().update()
		self.input()
		vel = self.direction
		if vel:
			vel.normalize_ip()
		self.body.linearVelocity = vel * self.speed
		
		self.attack_time = max(self.attack_time - 1, 0)
    	