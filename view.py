import pygame
import ww

class View:
	def __init__(self, target=None, debug=False):
		self.rect = pygame.Rect(0, 0, ww.SCREEN_WIDTH, ww.SCREEN_HEIGHT)
		self.target = target
		self.bg = ww.Images.view
		self.bg_rect = self.bg.get_rect(topleft=(0, 0))
		self.debug = debug
		self.clock = pygame.time.Clock()
		self.font = pygame.font.SysFont("Verdana", 20)

	def step(self):
		if self.target:
			self.rect.center = self.target.rect.center

	def draw(self):
		ww.screen.fill('#71ddee')
		clip_rect = self.bg_rect.clip(self.rect)
		screen_rect = clip_rect.move(-self.rect.left, -self.rect.top)
		inside_rect = clip_rect.move(-self.bg_rect.left, -self.bg_rect.top)
		ww.screen.blit(self.bg, screen_rect, inside_rect)

		for sprite in sorted(ww.group.sprites(), key=lambda sprite: sprite.rect.bottom):
			clip_rect = sprite.rect.clip(self.rect)
			screen_rect = clip_rect.move(-self.rect.left, -self.rect.top)
			inside_rect = clip_rect.move(-sprite.rect.left, -sprite.rect.top)
			ww.screen.blit(sprite.image, screen_rect, inside_rect)
		
		self.text = self.font.render(str(round(self.clock.get_fps(), 2)), True, (0, 0, 0))
		ww.screen.blit(self.text, (10, 10))
		self.clock.tick(60)