import pygame
import globals
import math

class Bullet(pygame.sprite.Sprite):
	def __init__(self, pos, life):
		super().__init__()
		self.life = life

		self.pos = pygame.math.Vector2(pos)
		self.image = globals.Images.bullet
		self.rect = self.image.get_rect(center=self.pos)

		self.speed = 15
		self.vel = pygame.math.Vector2(pygame.mouse.get_pos()) + globals.view.rect.topleft - pos
		rads = math.atan2(-self.vel.y, self.vel.x)
		degs = math.degrees(rads)
		self.image = pygame.transform.rotate(self.image, degs)
		self.vel = self.vel.normalize() * self.speed
		
	def update(self):
		self.pos += self.vel
		self.rect.center = self.pos
		self.mask = pygame.mask.from_surface(self.image)
		self.player_mask = pygame.mask.from_surface(globals.player.image)

		if self.life:
			self.life -= 1
		else:
			self.kill()

		if pygame.sprite.spritecollide(self, globals.tree_group, True, pygame.sprite.collide_mask):
			self.kill()