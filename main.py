import pygame, sys
from random import randint

# window size
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# enemy class
class Tree(pygame.sprite.Sprite):
	def __init__(self, pos):
		super().__init__()
		self.image = pygame.image.load('assets/tree.png').convert_alpha()
		self.rect = self.image.get_rect(topleft=pos)


	def update(self):
		if pygame.sprite.spritecollide(self, pygame.sprite.GroupSingle(player), False, pygame.sprite.collide_mask):
			self.kill()

# player class
class Player(pygame.sprite.Sprite):
	def __init__(self, pos):
		super().__init__()
		self.image = pygame.image.load('assets/player.png').convert_alpha()
		self.rect = self.image.get_rect(center=pos)
		self.direction = pygame.math.Vector2()
		self.speed = 5

	def input(self):
		# input key
		keys = pygame.key.get_pressed()

		# move
		if keys[pygame.K_w]:
			self.direction.y = -1
		elif keys[pygame.K_s]:
			self.direction.y = 1
		else:
			self.direction.y = 0

		if keys[pygame.K_d]:
			self.direction.x = 1
		elif keys[pygame.K_a]:
			self.direction.x = -1
		else:
			self.direction.x = 0
		
		# attack
		if pygame.mouse.get_pressed()[0]:
			group.add(Bullet(self.rect, view.rect.topleft))

	def update(self):
		self.input()
		self.rect.center += self.direction * self.speed
    		
# bullet class
class Bullet(pygame.sprite.Sprite):
	def __init__(self, player_pos, camera_pos):
		# set position, speed, velocity, some of physics variables
		super().__init__()
		self.image = pygame.Surface((10, 10))
		self.image.fill((255, 0, 0))
		self.pos = pygame.math.Vector2(player_pos.center)
		self.rect = self.image.get_rect(center=self.pos)

		self.speed = 15
		self.vel = pygame.math.Vector2(pygame.mouse.get_pos()) + camera_pos - player_pos.center
		self.vel = self.vel.normalize() * self.speed
		
	def update(self):
		# move
		self.pos += self.vel
		self.rect.center = self.pos

		# if collide with enemy, kill both objects
		if pygame.sprite.spritecollide(self, tree_group, True, pygame.sprite.collide_mask):
			self.kill()
		
# camera class
class View:
	def __init__(self, rect, target=None):
		self.rect = rect
		self.target = target
		self.bg = pygame.image.load('assets/ground.png').convert_alpha()
		self.bg_rect = self.bg.get_rect(topleft=(0, 0))

	def step(self):
		# camera move along with player
		if self.target:
			self.rect.center = self.target.rect.center

	def draw(self, group):
		# render all of objects in group
		global screen
		screen.fill('#71ddee')
		clip_rect = self.bg_rect.clip(self.rect)
		screen_rect = clip_rect.move(-self.rect.left, -self.rect.top)
		inside_rect = clip_rect.move(-self.bg_rect.left, -self.bg_rect.top)
		screen.blit(self.bg, screen_rect, inside_rect)

		# sort because represent depth
		for sprite in sorted(group.sprites(), key=lambda sprite: sprite.rect.bottom):
			clip_rect = sprite.rect.clip(self.rect)
			screen_rect = clip_rect.move(-self.rect.left, -self.rect.top)
			inside_rect = clip_rect.move(-sprite.rect.left, -sprite.rect.top)
			screen.blit(sprite.image, screen_rect, inside_rect)

# calculating fps and wait
class FPS:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Verdana", 20)
        self.text = self.font.render(str(self.clock.get_fps()), True, (0, 0, 0))
 
    def render(self, display):
        self.text = self.font.render(str(round(self.clock.get_fps(),2)), True, (0, 0, 0))
        display.blit(self.text, (10, 10))


# initial room settings
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
fps = FPS()

group = pygame.sprite.Group()
player = Player((640,360))
player_group = pygame.sprite.GroupSingle(player)
group.add(player_group)

view = View(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), player)
tree_group = pygame.sprite.Group()

for i in range(20):
	random_x = randint(0,1000)
	random_y = randint(0,1000)
	tree_group.add(Tree((random_x, random_y)))
group.add(tree_group)


# runtime loop
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()

	view.step()
	view.draw(group)
	group.update()
	fps.render(screen)
	pygame.display.update()
	fps.clock.tick(60)
