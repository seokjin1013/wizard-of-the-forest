import pygame
from monster import *
import ww

class View:
	def __init__(self, target=None, debug=False):
		self.rect = pygame.Rect(0, 0, ww.SCREEN_WIDTH, ww.SCREEN_HEIGHT)
		self.target = target
		self.bg = ww.backgrounds['stage1']
		self.bg_rect = self.bg.get_rect()
		self.debug = debug
		self.clock = pygame.time.Clock()
		self.font = pygame.font.SysFont("Verdana", 20)
		self.debug_text = []

	def update(self):
		if self.target:
			self.rect.center = self.target.pos

	def draw_debug_text(self):
		for idx, text in enumerate(self.debug_text):
			text = self.font.render(str(text), True, (0, 0, 0))
			ww.screen.blit(text, (10, 10 + idx * 20))
		self.debug_text.clear()

	def draw(self):
		ww.screen.fill('#71ddee')

		screen_rect = self.bg_rect.move(-self.rect.left, -self.rect.top)
		ww.screen.blit(self.bg, screen_rect)

		for sprite in ww.group.sprites():
			ww.group.change_layer(sprite, sprite.pos.y)
			sprite.rect.center = sprite.pos - self.rect.topleft
		
		ww.group.draw(ww.screen)
		
		for sprite in ww.group.sprites():
			if isinstance(sprite, Tree):
				hp_rect = pygame.Rect(sprite.rect.left, sprite.rect.bottom, sprite.rect.width, 8)
				pygame.draw.rect(ww.screen, (0, 0, 0), hp_rect, 0, 5)
				
				border = ww.HP_BAR_BORDER
				hp_rect = pygame.Rect(sprite.rect.left + border, sprite.rect.bottom + border,
									(sprite.rect.width - border * 2) * sprite.hp / sprite.mhp, 8 - border * 2)
				pygame.draw.rect(ww.screen, (255, 0, 0), hp_rect, 0, 5)

		for body in ww.world.bodies:
			for fixture in body.fixtures:
				vertices = [body.transform * v * ww.PPM - self.rect.topleft for v in fixture.shape.vertices]
				pygame.draw.polygon(ww.screen, (192, 32, 32), vertices, 2)
				
		
		self.debug_text.append(round(self.clock.get_fps(), 2))
		self.debug_text.append(len(ww.group))

		self.draw_debug_text()
		self.clock.tick(ww.FPS)