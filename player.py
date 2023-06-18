import pygame
from instance import Instance
import ww
from bullet import Bullet

class Player(Instance):
	def __init__(self, pos):
		super().__init__(pos)
		self.sprite_index = ww.sprites['player_idle']
		self.speed = 8
		self.mhp = 100
		self.hp = self.mhp
		self.attack_time = 0
		self.attack_delay = 4
		self.image_index = 0

		self.light_ambient = 0.5
		self.light_diffuse = 0.5

		

	def update(self):
		super().update()
		keys = pygame.key.get_pressed()

		self.direction = pygame.math.Vector2(
			keys[pygame.K_d] - keys[pygame.K_a],
			keys[pygame.K_s] - keys[pygame.K_w]
		)
		if self.direction:
			self.direction.normalize_ip()
		self.body.linearVelocity = self.direction * self.speed
			
		if pygame.mouse.get_pressed()[0] and self.attack_time == 0:
			ww.group.add(Bullet(self.pos))
			self.attack_time = self.attack_delay
		
		if keys[pygame.K_d] - keys[pygame.K_a] == 1:
			self.image_xscale = 1
		if keys[pygame.K_d] - keys[pygame.K_a] == -1:
			self.image_xscale = -1

		if (keys[pygame.K_d] or keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_w]) and self.sprite_index == ww.sprites['player_idle']:
			self.sprite_index = ww.sprites['player_run']
			self.image_index = 0

		if not (keys[pygame.K_d] or keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_w]) and self.sprite_index == ww.sprites['player_run']:
			self.sprite_index = ww.sprites['player_idle']
			self.image_index = 0
			
		self.attack_time = max(self.attack_time - 1, 0)
