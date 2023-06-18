from instance import LifeInstance
import ww
from Box2D import *
import numpy as np
from particle import Particle
import pygame

class Tree(LifeInstance):
	def __init__(self, pos):
		super().__init__(pos)
		self.sprite_index = ww.sprites['tree_idle']
		self.normals_index = ww.sprites['tree_idle_normal']
		self.speed = 5
		self.mhp = 10
		self.hp = self.mhp
		self.attack = 1
		self.gold = 5

	def apply_wave_strength(self):
		self.hp *= 1 + 0.1 * (ww.wave - 1)
		self.attack *= 1 + 0.1 * (ww.wave - 1)
		if ww.wave > 10:
			self.hp += (ww.wave - 10) * 2
			self.attack += (ww.wave - 10) * 2

	def update(self):
		if ww.phase == ww.PHASE.PLAY:
			vel = ww.player.pos - self.pos
		elif ww.phase == ww.PHASE.SHOP or ww.phase == ww.PHASE.DEAD:
			vel = -(ww.player.pos - self.pos)
			if not ww.view.rect.colliderect(self.aabb_rect):
				self.kill()
				return
		vel.Normalize()
		self.body.linearVelocity = vel * self.speed

		for ce in self.body.contacts:
			if ce.other.userData is ww.player:
				ce.other.userData.hp -= self.attack
				ce.other.userData.render_hit = True
				ce.other.userData.image_color_mul = 0, 0, 0, 1
				ce.other.userData.image_color_add = 1, 1, 1, 0
				break
		
		if vel.x > 0:
			self.image_scale.x = 1
		if vel.x < 0:
			self.image_scale.x = -1

		super().update()

	def dead(self):
		for _ in range(np.random.randint(15, 20)):
			dir = np.random.uniform(0, 360)
			spd = abs(np.random.normal(0, 6))
			vel = pygame.Vector2(np.cos(dir) * spd, np.sin(dir) * spd)
			ww.group.add(Particle(ww.sprites['particle'], self.pos, vel, dur=10, image_color_mul=(1, 0, 0, 1), dspd=0.8))
			ww.view.add_shake(0.07, 0.07)
		ww.player.gold += self.gold * ww.player.stat.gold_earn
		ww.player.hp = min(ww.player.hp + ww.player.items_tier3[9], ww.player.stat.mhp)
		pygame.mixer.find_channel(True).play(ww.sounds['dead'])
		super().dead()


class Slime(Tree):
	def __init__(self, pos):
		super().__init__(pos)
		self.sprite_index = ww.sprites['슬라임']
		self.normals_index = None
		self.mhp = 7
		self.speed = 3
		self.attack = 1
		self.gold = 2
		self.hp = self.mhp
		self.apply_wave_strength()

class Bat(Tree):
	def __init__(self, pos):
		super().__init__(pos)
		self.sprite_index = ww.sprites['박쥐']
		self.normals_index = None
		self.mhp = 4
		self.speed = 5
		self.attack = 1
		self.gold = 1
		self.hp = self.mhp
		self.apply_wave_strength()

class Wolf(Tree):
	def __init__(self, pos):
		super().__init__(pos)
		self.sprite_index = ww.sprites['늑대']
		self.normals_index = None
		self.mhp = 11
		self.speed = 6
		self.attack = 1
		self.gold = 4
		self.hp = self.mhp
		self.apply_wave_strength()

class Skelleton(Tree):
	def __init__(self, pos):
		super().__init__(pos)
		self.sprite_index = ww.sprites['스켈레톤']
		self.normals_index = None
		self.mhp = 8
		self.speed = 4
		self.attack = 2
		self.gold = 3
		self.hp = self.mhp
		self.apply_wave_strength()