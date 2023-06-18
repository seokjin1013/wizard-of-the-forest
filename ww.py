import pygame
import Box2D
import math
from pygame.locals import *
from monster import *
from player import Player
from m1Attack import M1Attack, M2Attack
from enum import IntEnum, Enum, auto
from monster.tree import *

WINDOW_SIZE = pygame.Vector2(1920, 1080)
# WINDOW_SIZE = pygame.Vector2(1280, 720)
SCREEN_SIZE = pygame.Vector2(640, 360)
FPS = 60
PPM = 20
DEBUG = False

class PHASE(Enum):
	TITLE = auto()
	PLAY = auto()
	SHOP = auto()
	DEAD = auto()
	CLEAR = auto()

phase = PHASE.TITLE
wave = 1

pygame.init()
pygame.display.set_mode(WINDOW_SIZE, flags=pygame.DOUBLEBUF | pygame.OPENGL | pygame.FULLSCREEN)
# pygame.display.set_mode(WINDOW_SIZE, flags=pygame.DOUBLEBUF | pygame.OPENGL, vsync=1)

font20 = pygame.font.Font("SCDream6.otf", 20)
font15 = pygame.font.Font("SCDream6.otf", 15)
font12 = pygame.font.Font("SCDream6.otf", 12)

world = Box2D.b2World(gravity=(0, 0))

backgrounds = {
	'stage1': pygame.image.load('ground.png').convert_alpha()
}

import pathlib
import json
import os

# load all of resources first only one

# abstraction of graphics
class Sprite:
	def __init__(self, path: pathlib.Path):
		paths = path.glob('*.png')
		paths = sorted(paths, key=lambda x: int(x.stem))
		self.images = [
			pygame.image.load(path).convert_alpha()
			for path in paths
		]
		if os.path.isfile(path / 'meta.json'):
			data = json.loads((path / 'meta.json').read_text())
			for key, value in data.items():
				setattr(self, key, value)
		if not hasattr(self, 'l'):
			self.l = 0
		if not hasattr(self, 'r'):
			self.r = self.images[0].get_width()
		if not hasattr(self, 't'):
			self.t = 0
		if not hasattr(self, 'b'):
			self.b = self.images[0].get_height()
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

sounds = {
	sound_path.stem : pygame.mixer.Sound(sound_path)
	for sound_path in pathlib.Path('sounds').glob('*.wav')
}
for sound in sounds.values():
	sound.set_volume(0.1)
pygame.mixer.set_num_channels(60)
pygame.mixer.music.load('sounds/bgm.mp3')
pygame.mixer.music.play(-1)

def _get_ellipsis_vertices(sprite):
	precision = 8
	vertices = []
	for i in range(precision):
		angle = math.pi * 2 / precision * i
		x = (math.cos(angle) * sprite.w / 2) / PPM
		y = (math.sin(angle) * sprite.h / 2) / PPM
		vertices.append([x, y])
	return vertices

# collision cateogory
class CategoryBits(IntEnum):
	PLAYER  = 0b0000_0000_0000_0001
	BULLET  = 0b0000_0000_0000_0010
	MONSTER = 0b0000_0000_0000_0100

basic_sprite = {
	Player: sprites['player_idle'],
	Tree: sprites['tree_idle'],
	M1Attack: sprites['skill_effect_m1'],
	M2Attack: sprites['skill_effect_m2'],
}

# attach fixture to objects for collision checking and allocate collision category
fixture_defs = {
	Player: Box2D.b2FixtureDef(
		density=100.0, categoryBits=CategoryBits.PLAYER, maskBits=CategoryBits.MONSTER,
		shape=Box2D.b2PolygonShape(vertices=_get_ellipsis_vertices(basic_sprite[Player])),
	),
	Tree: Box2D.b2FixtureDef(
		density=0.1, categoryBits=CategoryBits.MONSTER, maskBits=CategoryBits.PLAYER | CategoryBits.MONSTER | CategoryBits.BULLET,
		shape=Box2D.b2PolygonShape(vertices=_get_ellipsis_vertices(basic_sprite[Tree])),
	),
	Slime: Box2D.b2FixtureDef(
		density=0.1, categoryBits=CategoryBits.MONSTER, maskBits=CategoryBits.PLAYER | CategoryBits.MONSTER | CategoryBits.BULLET,
		shape=Box2D.b2PolygonShape(vertices=_get_ellipsis_vertices(basic_sprite[Tree])),
	),
	Bat: Box2D.b2FixtureDef(
		density=0.1, categoryBits=CategoryBits.MONSTER, maskBits=CategoryBits.PLAYER | CategoryBits.MONSTER | CategoryBits.BULLET,
		shape=Box2D.b2PolygonShape(vertices=_get_ellipsis_vertices(basic_sprite[Tree])),
	),
	Wolf: Box2D.b2FixtureDef(
		density=0.1, categoryBits=CategoryBits.MONSTER, maskBits=CategoryBits.PLAYER | CategoryBits.MONSTER | CategoryBits.BULLET,
		shape=Box2D.b2PolygonShape(vertices=_get_ellipsis_vertices(basic_sprite[Tree])),
	),
	Skelleton: Box2D.b2FixtureDef(
		density=0.1, categoryBits=CategoryBits.MONSTER, maskBits=CategoryBits.PLAYER | CategoryBits.MONSTER | CategoryBits.BULLET,
		shape=Box2D.b2PolygonShape(vertices=_get_ellipsis_vertices(basic_sprite[Tree])),
	),
	M1Attack: Box2D.b2FixtureDef(
		density=0.1, categoryBits=CategoryBits.BULLET, maskBits=CategoryBits.MONSTER,
		shape=Box2D.b2PolygonShape(vertices=_get_ellipsis_vertices(basic_sprite[M1Attack])),
	),
	M2Attack: Box2D.b2FixtureDef(
		density=0.1, categoryBits=CategoryBits.BULLET, maskBits=CategoryBits.MONSTER,
		shape=Box2D.b2PolygonShape(vertices=_get_ellipsis_vertices(basic_sprite[M2Attack])),
	),
}