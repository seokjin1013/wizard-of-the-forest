from instance import Instance
import ww
from Box2D import *

class Tree(Instance):
	def __init__(self, pos):
		super().__init__(pos)
		self.sprite_index = ww.sprites['tree_idle']
		self.normals_index = ww.sprites['tree_idle_normal']
		self.speed = 5
		self.mhp = 5
		self.hp = self.mhp

	def update(self):
		super().update()
		vel = ww.player.pos - self.pos
		vel.Normalize()
		self.body.linearVelocity = vel * self.speed

		if self.hp <= 0:
			self.kill()