import pygame
import ww
import math

class Bullet(pygame.sprite.Sprite):
	def __init__(self, pos, life):
		super().__init__()
		self.life = life

		self.pos = pygame.math.Vector2(pos)
		self.image = ww.Images.bullet
		self.rect = self.image.get_rect(center=self.pos)

		self.speed = 15
		self.vel = pygame.math.Vector2(pygame.mouse.get_pos()) + ww.view.rect.topleft - pos
		rads = math.atan2(-self.vel.y, self.vel.x)
		degs = math.degrees(rads)
		self.image = pygame.transform.rotate(self.image, degs)
		self.vel = self.vel.normalize() * self.speed
		
	def update(self):
		self.pos += self.vel
		self.rect.center = self.pos
		self.mask = pygame.mask.from_surface(self.image)
		self.player_mask = pygame.mask.from_surface(ww.player.image)

		if self.life:
			self.life -= 1
		else:
			self.kill()

		collided = pygame.sprite.spritecollide(self, ww.tree_group, False, pygame.sprite.collide_mask)
		if collided:
			for sprite in collided:
				sprite.hp -= 1
			self.kill()