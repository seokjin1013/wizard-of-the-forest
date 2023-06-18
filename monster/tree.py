import pygame
import globals

class Tree(pygame.sprite.Sprite):
	def __init__(self, pos):
		super().__init__()
		self.pos = pygame.Vector2(pos)
		self.image = globals.Images.tree
		self.rect = self.image.get_rect(topleft=pos)

		self.speed = 1

	def update(self):
		vel = pygame.math.Vector2(globals.player.rect.center) - self.rect.center
		vel = vel.normalize() * self.speed
		self.pos += vel
		self.rect.center = self.pos
		if pygame.sprite.spritecollide(self, globals.player_group, False, pygame.sprite.collide_mask):
			self.kill()