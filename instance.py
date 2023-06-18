import pygame
import ww
import Box2D
import numpy as np

class Instance(pygame.sprite.Sprite):
	def __init__(self, pos):
		super().__init__()
		self.sprite_index = None
		self.normals_index = None
		self.image_index = 0
		self.image_speed = 0.2
		self.image_angle = 0
		self.image_xscale = 1
		self.image_yscale = 1
		self.light_ambient = 0
		self.light_diffuse = 0

		self.pos = Box2D.b2Vec2(pos)
		self.body = ww.world.CreateDynamicBody(position=self.pos/ww.PPM)
		self.body.CreateFixture(ww.fixture_defs[self.__class__])
		self.body.fixedRotation = True
		self.body.userData = self

	def update(self):
		self.pos = self.body.transform.position * ww.PPM
		self.image_index = (self.image_index + self.image_speed) % len(self.sprite_index)

	def get_image(self):
		if not self.sprite_index:
			return None
		return self.sprite_index[int(self.image_index)]

	def get_normali(self):
		if not self.normals_index:
			return None
		return self.normals_index[int(self.image_index)]

	def get_quad(self):
		R = np.identity(3)
		R[0][0] = R[1][1] = np.cos(self.image_angle)
		R[1][0] = np.sin(self.image_angle)
		R[0][1] = -R[1][0]
		S = np.identity(3)
		S[0][0], S[1][1] = self.image_xscale, self.image_yscale
		T = np.identity(3)
		T[0][2], T[1][2] = np.floor(self.pos)
		P = np.ones((3, 4))
		rect = self.get_image().get_rect(topleft=(-self.sprite_index.x, -self.sprite_index.y))
		P[0][0], P[1][0] = rect.left, rect.top
		P[0][1], P[1][1] = rect.right, rect.top
		P[0][2], P[1][2] = rect.right, rect.bottom
		P[0][3], P[1][3] = rect.left, rect.bottom
		return (T @ R @ S @ P)[:2,:].T

	def get_vertices(self):
		return np.array([self.body.transform * v * ww.PPM for v in self.body.fixtures[0].shape.vertices])
	
	def get_aabb_rect(self):
		aabb = self.body.fixtures[0].GetAABB(0)
		lt = aabb.lowerBound * ww.PPM
		wh = (aabb.upperBound - aabb.lowerBound) * ww.PPM
		rect = pygame.Rect(*lt, *wh)
		return rect

	def kill(self):
		ww.world.DestroyBody(self.body)
		super().kill()