import pygame
import ww
import numpy as np

# all of instance
class Instance(pygame.sprite.Sprite):
	def __init__(self, pos):
		super().__init__()
		self.pos = pygame.Vector2(pos)
		
		
# drawable in surface screen
class DrawableInstance(Instance):
	def __init__(self, pos):
		super().__init__(pos)
		self.sprite_index = None
		self.normals_index = None
		self.image_index = 0
		self.image_speed = 0.2
		self.image_angle = 0
		self.image_scale = pygame.Vector2(1, 1)
		self.image_color_mul = 1, 1, 1, 1
		self.image_color_add = 0, 0, 0, 0

	def update(self):
		super().update()
		self.image_index = (self.image_index + self.image_speed) % len(self.sprite_index)

	@property
	def image(self):
		return self.sprite_index[int(self.image_index)]

	@property
	def quad(self):
		R = np.identity(3)
		R[0][0] = R[1][1] = np.cos(self.image_angle)
		R[1][0] = np.sin(self.image_angle)
		R[0][1] = -R[1][0]
		S = np.identity(3)
		S[0][0], S[1][1] = self.image_scale
		T = np.identity(3)
		T[0][2], T[1][2] = np.floor(self.pos)
		P = np.ones((3, 4))
		rect = self.image.get_rect(topleft=(-self.sprite_index.x, -self.sprite_index.y))
		P[0][0], P[1][0] = rect.left, rect.top
		P[0][1], P[1][1] = rect.right, rect.top
		P[0][2], P[1][2] = rect.right, rect.bottom
		P[0][3], P[1][3] = rect.left, rect.bottom
		return (T @ R @ S @ P)[:2,:].T

	@property
	def normal(self):
		if not self.normals_index:
			return None
		return self.normals_index[int(self.image_index)]


# collidable, monster or player etc.
class CollidableInstance(Instance):
	def __init__(self, pos):
		super().__init__(pos)
		self.body = ww.world.CreateDynamicBody(position=self.pos/ww.PPM)
		self.body.CreateFixture(ww.fixture_defs[self.__class__])
		self.body.fixedRotation = True
		self.body.userData = self

	def update(self):
		super().update()
		self.pos = self.body.transform.position * ww.PPM

	@property
	def aabb_rect(self):
		aabb = self.body.fixtures[0].GetAABB(0)
		lt = aabb.lowerBound * ww.PPM
		wh = (aabb.upperBound - aabb.lowerBound) * ww.PPM
		rect = pygame.Rect(*lt, *wh)
		return rect

	@property
	def vertices(self):
		return np.array([self.body.transform * v * ww.PPM for v in self.body.fixtures[0].shape.vertices])
	
	def kill(self):
		ww.world.DestroyBody(self.body)
		super().kill()


# self-light objects like lightening or skill effects
class BrightInstance(Instance):
	def __init__(self, pos):
		super().__init__(pos)
		self.light_diffuse = 0
		self.light_color = pygame.Vector3(1, 1, 1)

	def kill(self):
		super().kill()


# like monster, player.
class LifeInstance(CollidableInstance, DrawableInstance):
	def __init__(self, pos):
		super().__init__(pos)
		self.render_hit = False
		self.mhp = 100
		self.hp = 100

	def update(self):
		if self.hp <= 0:
			self.dead()
		if self.render_hit:
			self.image_color_mul = 0, 0, 0, 1
			self.image_color_add = 1, 1, 1, 0
			self.render_hit = False
		else:
			self.image_color_mul = 1, 1, 1, 1
			self.image_color_add = 0, 0, 0, 0
		super().update()

	def dead(self):
		self.kill()

	@property
	def normal(self):
		if not self.normals_index or self.render_hit:
			return None
		return self.normals_index[int(self.image_index)]


# like particle effects
class TemporaryInstance(Instance):
	def __init__(self, pos):
		super().__init__(pos)
		self.t = 0
		self.dur = 10

	def update(self):
		self.t += 1
		if self.t >= self.dur:
			self.kill()
		super().update()


# just bullet, quick and short duration
class BulletInstance(TemporaryInstance, CollidableInstance, DrawableInstance):
	def __init__(self, pos):
		super().__init__(pos)
		self.speed = 40
		self.vel = ww.controller.mouse_pos - pos or pygame.Vector2(1, 0)
		self.vel = self.vel / np.linalg.norm(self.vel) * self.speed
		self.attack = 1
		self.body.bullet = True

	def update(self):
		self.body.linearVelocity = self.vel
		super().update()