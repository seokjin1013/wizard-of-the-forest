import pygame
import ww

class Tree(pygame.sprite.Sprite):
	def __init__(self, pos):
		super().__init__()
		self.pos = pygame.Vector2(pos)
		self.image = ww.Images.tree
		self.rect = self.image.get_rect(topleft=pos)
		self.speed = 1
		self.mhp = 5
		self.hp = self.mhp

	def update(self):
		vel = ww.player.pos - self.pos
		vel = vel.normalize() * self.speed

		for x in ww.tree_group.sprites():
			if x is self:
				continue
			if self.rect.colliderect(x.rect):
				vel = pygame.math.Vector2(x.rect.center) - pygame.math.Vector2(self.rect.center)
				vel = vel.normalize() * self.speed * -3
				break

		self.pos += vel
		self.rect.center = self.pos
		if self.hp == 0:
			self.kill()