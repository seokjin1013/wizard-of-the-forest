from instance import LifeInstance, BrightInstance, DrawableInstance
import ww
from m1Attack import M1Attack, M2Attack
import pygame
from monster import *
from item import *
from particle import Particle2
import numpy as np

class Player(LifeInstance, BrightInstance):
	def __init__(self, pos):
		super().__init__(pos)
		self.sprite_index = ww.sprites['player_idle']

		self.stat = Status()
		self.base_stat = Status()

		# 변동된 값 #
		self.hp = self.stat.mhp # 현재 체력
		self.gold = 0 # 현재 골드
		self.skill_point = 1
		self.skill_level = [0, 0, 0]
		self.items_tier3 = [0 for _ in range(len(items_tier3_name))] # 획득한 아이템

		self.m1Attack_time = 0
		self.m2Attack_time = 0
		self.shift_time = 0
		self.image_index = 0

		self.reroll_cnt = 0

		self.light_diffuse = 0.5

	def apply_item(self):
		# 아이템 능력치를 적용하여 최종능력치를 갱신 #
		self.stat.atk = self.base_stat.atk
		self.stat.atk_firerate = self.base_stat.atk_firerate
		self.stat.speed = self.base_stat.speed
		self.stat.mhp = self.base_stat.mhp
		self.stat.atk_velocity= self.base_stat.atk_velocity
		self.stat.atk_duration= self.base_stat.atk_duration
		self.stat.crit = self.base_stat.crit
		self.stat.crit_atk = self.base_stat.crit_atk
		self.stat.gold_earn = self.base_stat.gold_earn

		self.stat.atk += self.items_tier3[0]
		self.stat.atk *= (1 + self.items_tier3[1] * 0.05)
		self.stat.mhp += self.items_tier3[2] * 10
		self.stat.mhp *= (1 + self.items_tier3[3] * 0.05)
		self.stat.atk_firerate *= (1 + self.items_tier3[4] * 0.1)
		self.stat.atk_velocity *= (1 + self.items_tier3[5] * 0.1)
		self.stat.atk_duration *= (1 + self.items_tier3[6] * 0.1)
		self.stat.atk_duration *= (1 + self.items_tier3[7] * -0.15)
		self.stat.atk_firerate *= (1 + self.items_tier3[7] * 0.15)
		self.stat.atk_velocity *= (1 + self.items_tier3[8] * -0.15)
		self.stat.atk *= (1 + self.items_tier3[8] * 0.1)
		self.stat.atk_velocity *= (1 + self.items_tier3[10] * 0.06)
		self.stat.atk *= (1 + self.items_tier3[10] * 0.03)
		self.stat.crit += self.items_tier3[11] * 0.08
		self.stat.crit_atk *= (1 + self.items_tier3[12] * 0.05)
		self.stat.speed *= (1 + self.items_tier3[13] * 0.1)

	def update(self):
		super().update()

		if ww.phase == ww.PHASE.PLAY:
			self.direction = ww.controller.direction
			self.body.linearVelocity = self.direction * self.stat.speed
				
			if ww.controller.mouse_left_down and self.m1Attack_time <= 0:
				ww.group.add(M1Attack(self.pos - (0, 12), self.stat))
				self.m1Attack_time += 1
			if ww.controller.mouse_right_pressed and self.m2Attack_time <= 0:
				ww.group.add(M2Attack(ww.controller.mouse_pos, self.stat))
				self.m2Attack_time += 1
			if ww.controller.shift and self.shift_time <= 0:
				ww.group.add(Particle2(ww.sprites['skill_effect_shift'], pos=self.pos + (0, -10), dur=30, image_scale=(2,2)))
				dist = ww.controller.mouse_pos - self.pos or pygame.Vector2(1, 0)
				dist = dist / np.linalg.norm(dist) * 5
				self.body.position += dist
				self.shift_time += 1
		else:
			self.body.linearVelocity = (0, 0)
		
		if ww.controller.horizontal == 1:
			self.image_scale.x = 1
		if ww.controller.horizontal == -1:
			self.image_scale.x = -1
			
		if ww.controller.direction and self.sprite_index == ww.sprites['player_idle']:
			self.sprite_index = ww.sprites['player_run']
			self.image_index = 0

		if not ww.controller.direction and self.sprite_index == ww.sprites['player_run']:
			self.sprite_index = ww.sprites['player_idle']
			self.image_index = 0
			
		self.m1Attack_time = max(self.m1Attack_time - self.stat.atk_firerate / ww.FPS, 0)
		
		self.m2Attack_time = max(self.m2Attack_time - 1 / (13 - (ww.player.skill_level[1]) // 2 * 0.5) / ww.FPS, 0)
		self.shift_time = max(self.shift_time - 1 / (25 - ww.player.skill_level[2] * 0.7) / ww.FPS, 0)

	def kill(self):
		ww.group.add(PlayerDeath(self))
		ww.view.add_flash()
		ww.view.add_shake(3, 3)
		ww.phase = ww.PHASE.DEAD
		super().kill()


class PlayerDeath(DrawableInstance, BrightInstance):
	def __init__(self, player):
		super().__init__(player.pos)
		self.sprite_index = ww.sprites['player_death']
		self.image_index = 0
		self.image_speed = 0.05
		self.image_scale = player.image_scale

		self.light_diffuse = 0.5
		self.light_color = pygame.Vector3(1, 1, 1)
		pygame.mixer.find_channel(True).play(ww.sounds['gameover'])
	
	def update(self):
		self.light_color.yz *= 0.995
		if self.image_index >= len(self.sprite_index.images) - 1:
			self.image_speed = 0
		super().update()