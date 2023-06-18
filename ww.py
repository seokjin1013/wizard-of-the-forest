import pygame
import Box2D
import math
from pygame.locals import *
from monster import *
from player import Player
from bullet import Bullet
from enum import IntEnum

WINDOW_SIZE = (1920, 1080)
SCREEN_SIZE = (640, 360)
FPS = 60
PPM = 20
DEBUG = True

pygame.init()
pygame.display.set_mode(WINDOW_SIZE, flags=pygame.DOUBLEBUF | pygame.OPENGL | pygame.FULLSCREEN, vsync=1)

world = Box2D.b2World(gravity=(0, 0))

backgrounds = {
	'stage1': pygame.image.load('ground.png').convert_alpha()
}

import pathlib
import json

class Sprite:
	def __init__(self, path: pathlib.Path):
		self.images = [
			pygame.image.load(path).convert_alpha()
			for path in path.glob('*.png')
		]
		data = json.loads((path / 'meta.json').read_text())
		for key, value in data.items():
			setattr(self, key, value)
		if not hasattr(self, 'x'):
			self.x = (self.l + self.r) // 2
		if not hasattr(self, 'y'):
			self.y = (self.t + self.b) // 2
		if not hasattr(self, 'w'):
			self.w = self.r - self.l
		if not hasattr(self, 'h'):
			self.h = self.b - self.t

	def __getitem__(self, index):
		return self.images[index]

	def __len__(self):
		return len(self.images)

sprites = {
    sprite_path.name : Sprite(sprite_path)
    for sprite_path in pathlib.Path('assets').glob('*')
}

# define collision shape
def _get_ellipsis_vertices(cls, pos, size):
    precision = 16

def _get_ellipsis_vertices(sprite):
	precision = 8
	vertices = []
	for i in range(precision):
		angle = math.pi * 2 / precision * i
		x = (math.cos(angle) * sprite.w / 2) / PPM
		y = (math.sin(angle) * sprite.h / 2) / PPM
		vertices.append(Box2D.b2Vec2(x, y))
	return vertices

# define collision type
class category_bits(IntEnum):
	PLAYER  = 0b0000_0000_0000_0001
	BULLET  = 0b0000_0000_0000_0010
	MONSTER = 0b0000_0000_0000_0100
	
# attach object to fixture to do collision check
basic_sprite = {
	Player: sprites['player_idle'],
	Tree: sprites['tree_idle'],
	Bullet: sprites['bullet_idle'],
}

fixture_defs = {
	Player: Box2D.b2FixtureDef(
		density=100.0, categoryBits=category_bits.PLAYER, maskBits=category_bits.MONSTER,
		shape=Box2D.b2PolygonShape(vertices=_get_ellipsis_vertices(basic_sprite[Player])),
	),
	Tree: Box2D.b2FixtureDef(
		density=0.1, categoryBits=category_bits.MONSTER, maskBits=category_bits.PLAYER | category_bits.MONSTER | category_bits.BULLET,
		shape=Box2D.b2PolygonShape(vertices=_get_ellipsis_vertices(basic_sprite[Tree])),
	),
	Bullet: Box2D.b2FixtureDef(
		density=0.1, categoryBits=category_bits.BULLET, maskBits=category_bits.MONSTER,
		shape=Box2D.b2PolygonShape(vertices=_get_ellipsis_vertices(basic_sprite[Bullet])),
	),
}