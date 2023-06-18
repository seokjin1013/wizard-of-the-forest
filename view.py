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
		
		for sprite in sorted(ww.group, key=lambda sprite: sprite.rect.bottom):
			clip_rect = sprite.rect.clip(self.rect)
			screen_rect = clip_rect.move(-self.rect.left, -self.rect.top)
			inside_rect = clip_rect.move(-sprite.rect.left, -sprite.rect.top)
			ww.screen.blit(sprite.image, screen_rect, inside_rect)
		
		for sprite in sorted(ww.tree_group, key=lambda sprite: sprite.rect.bottom):
			hp_rect = pygame.Rect(sprite.rect.left, sprite.rect.bottom, sprite.rect.width, 10)
			clip_rect = hp_rect.clip(self.rect)
			pygame.draw.rect(ww.screen, (0, 0, 0), clip_rect.move(-self.rect.left, -self.rect.top), 0)
			
			border = ww.HP_BAR_BORDER
			hp_rect = pygame.Rect(sprite.rect.left + border, sprite.rect.bottom + border,
								  (sprite.rect.width - border * 2) * sprite.hp / sprite.mhp, 10 - border * 2)
			clip_rect = hp_rect.clip(self.rect)
			pygame.draw.rect(ww.screen, (255, 0, 0), clip_rect.move(-self.rect.left, -self.rect.top), 0)
		
		self.text = self.font.render(str(round(self.clock.get_fps(), 2)), True, (0, 0, 0))
		ww.screen.blit(self.text, (10, 10))
		self.clock.tick(60)