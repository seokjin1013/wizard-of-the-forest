import pygame
import ww
from monster import *
import moderngl
import numpy as np
from instance import BrightInstance, LifeInstance, DrawableInstance, CollidableInstance
from particle import Particle
from damage_number import DamageNumber
from shop import Shop, ShopButton
from player import Player


# many of shading or shaking or color overlay or screen effect
class View:
	MAX_NUM_LIGHT = 60
	SHAKE_INTERVAL = 3
	FLASH_DURATION = 10
	NIGHT_LENGTH = 60 * 30
	def __init__(self, target=None):
		self.rect = pygame.Rect((0, 0), ww.SCREEN_SIZE)
		self.target = target

		self.shake = pygame.Vector2(0, 0)
		self.shake_t = 0
		self.shake_pos = pygame.Vector2(0, 0)
		self.shake_target = pygame.Vector2(0, 0)

		self.flash = 0
		self.flash_t = View.FLASH_DURATION

		self.time = 0
		self.ambient = [0.3, 0.3, 0.3]

		self.bg = ww.backgrounds['stage1']
		self.screen_quad = np.array([[-1, 1], [1, 1], [1, -1], [-1, -1]])
		self.debug_text = []

		self.ctx = moderngl.create_context()
		self.ctx.enable_only(moderngl.BLEND)

		# shader GLSL
		self.shader_basic = self.ctx.program(
			vertex_shader="""
				#version 330
				in vec2 in_uv;
				in vec2 in_position;
				out vec2 v_uv;
				void main()
				{
					gl_Position = vec4(in_position, 0.0, 1.0);
					v_uv = in_uv;
				}
			""",
			fragment_shader="""
				#version 330
				out vec4 fragColor;
				uniform sampler2D u_texture;
				uniform vec4 imageColorMul;
				uniform vec4 imageColorAdd;
				in vec2 v_uv;
				void main() 
				{
					fragColor = texture(u_texture, v_uv);
					fragColor = fragColor * imageColorMul + imageColorAdd;
				}
			"""
		)
		self.shader_light = self.ctx.program(
			vertex_shader="""
				#version 330
				in vec2 in_position;
				in vec2 in_uv;
				out vec2 v_uv;
				out vec2 fragPos;
				void main()
				{
					gl_Position = vec4(in_position, 0.0, 1.0);
					v_uv = in_uv;
					fragPos = in_position;
				}
			""",
			fragment_shader="""
				#version 330
				struct Light {
					vec3 position;
					vec3 color;
				
					vec3 diffuse;
					
					float constant;
					float linear;
					float quadratic;
				};

				in vec2 v_uv;
				in vec2 fragPos;
				out vec4 fragColor;
				uniform sampler2D u_texture;
				uniform sampler2D u_normal;
				uniform Light light[%d];
				uniform int numLight;
				uniform vec4 flashColor;
				uniform vec3 ambient;

				vec3 CalcPointLight(Light light, vec3 normal, vec3 fragPos)
				{
					vec3 lightDir = normalize(light.position - fragPos);
					
					float diff = max(dot(normal, lightDir), 0.0);
					
					float distance    = length(light.position - fragPos);
					float attenuation = 1.0 / (light.constant + light.linear * distance + 
								light.quadratic * (distance * distance));    
					
					vec3 diffuse = light.diffuse  * diff * texture(u_texture, v_uv).rgb;
					diffuse *= attenuation;
					return diffuse * light.color;
				}

				void main()
				{
					vec3 norm = normalize(texture(u_normal, v_uv).xyz - vec3(0.5, 0.5, 0.5));
					norm.x = -norm.x;
					vec3 result = vec3(0, 0, 0);
					result += ambient * texture(u_texture, v_uv).rgb;
					for(int i = 0; i < numLight; i++)
						result += CalcPointLight(light[i], norm, vec3(fragPos.xy, 0.0));
					result = result * (1 - flashColor.a) + flashColor.rgb * flashColor.a;
					fragColor = vec4(result, 1.0);
					flashColor;
				}
			""" % View.MAX_NUM_LIGHT
		)
		self.shader_light['u_texture'] = 0
		self.shader_light['u_normal'] = 1

		# define vertex buffer object or array object or buffer and layer
		self.vbo = self.ctx.buffer(None, reserve=4 * 4 * 4)
		self.vao_basic = self.ctx.vertex_array(self.shader_basic, [(self.vbo, "2f4 2f4", "in_position", "in_uv")], mode=moderngl.TRIANGLE_FAN)

		images = []
		for image in ww.backgrounds.values():
			images.append(image)
		for sprite in ww.sprites.values():
			for image in sprite:
				images.append(image)

		self.textures = {}
		for image in images:
			texture = self.ctx.texture(image.get_size(), 4, image.get_buffer())
			texture.swizzle = 'BGRA'
			texture.filter = moderngl.NEAREST, moderngl.NEAREST
			self.textures[image] = texture

		self.pg_screen = pygame.Surface(self.rect.size, flags=pygame.SRCALPHA)
		self.pg_texture = self.ctx.texture(self.rect.size, 4)
		self.pg_texture.filter = moderngl.NEAREST, moderngl.NEAREST
		self.pg_post_screen = pygame.Surface(self.rect.size, flags=pygame.SRCALPHA)
		self.pg_post_texture = self.ctx.texture(self.rect.size, 4)
		self.pg_post_texture.filter = moderngl.NEAREST, moderngl.NEAREST

		self.texture_layer = self.ctx.texture(self.rect.size, 4)
		self.texture_layer.filter = moderngl.NEAREST, moderngl.NEAREST
		self.texture_layer_fbo = self.ctx.framebuffer(self.texture_layer)
		self.normal_layer = self.ctx.texture(self.rect.size, 4)
		self.normal_layer.filter = moderngl.NEAREST, moderngl.NEAREST
		self.normal_layer_fbo = self.ctx.framebuffer(self.normal_layer)
		self.ui_layer = self.ctx.texture(self.rect.size, 4)
		self.ui_layer.filter = moderngl.NEAREST, moderngl.NEAREST
		self.ui_layer_fbo = self.ctx.framebuffer(self.ui_layer)
		self.vao_light = self.ctx.vertex_array(self.shader_light, [(self.vbo, "2f4 2f4", "in_position", "in_uv")], mode=moderngl.TRIANGLE_FAN)

	def add_shake(self, x, y):
		self.shake += x, y
		self.shake_t = View.SHAKE_INTERVAL

	def add_flash(self):
		self.flash_t = 0

	def update(self):
		if self.shake_t >= View.SHAKE_INTERVAL:
			dir = np.random.uniform(0, 360)
			self.shake_target = pygame.Vector2(np.cos(dir) * self.shake.x, np.sin(dir) * self.shake.y)
			self.shake_t = 0
		self.shake_pos = (self.shake_target + self.shake_pos) / 2

		if self.target:
			self.rect.center = self.target.pos + self.shake_pos
		self.shake *= 0.9
		self.shake_t += 1

		if self.flash_t < View.FLASH_DURATION:
			self.flash = (np.cos(self.flash_t / View.FLASH_DURATION * np.pi) + 1) / 2
			self.flash_t += 1
		else:
			self.flash = 0

		if ww.phase == ww.PHASE.PLAY:
			self.time += 1
			self.ambient[0] = max(self.ambient[0] - 0.004, 0.3)
			self.ambient[1] = max(self.ambient[1] - 0.004, 0.3)
			self.ambient[2] = max(self.ambient[2] - 0.004, 0.3)
		if self.time >= View.NIGHT_LENGTH:
			ww.phase = ww.PHASE.SHOP
			ww.group.add(Shop(self.rect.center))
		if ww.phase == ww.PHASE.SHOP or ww.phase == ww.PHASE.TITLE:
			self.ambient[0] = min(self.ambient[0] + 0.004, 0.8)
			self.ambient[1] = min(self.ambient[1] + 0.004, 0.8)
			self.ambient[2] = min(self.ambient[2] + 0.004, 0.8)

			self.time = 0
		self.debug_text.append(self.time)

	def draw_debug_text(self):
		for idx, text in enumerate(self.debug_text):
			text = ww.font20.render(str(text), False, (0, 0, 0))
			self.pg_screen.blit(text, (10, 10 + idx * 20))
		self.debug_text.clear()

	def draw(self):
		def rect_to_quad(rect: pygame.Rect) -> np.ndarray:
			return np.array([rect.topleft, rect.topright, rect.bottomright, rect.bottomleft])

		def gl_scaling(quad: np.ndarray) -> np.ndarray:
			quad = (quad - self.rect.topleft) / ww.SCREEN_SIZE * 2 - 1
			return quad
		
		def attach_uv(quad: np.ndarray) -> np.ndarray:
			uv = np.array([
				[0, 0], [1, 0], [1, 1], [0, 1],
			])
			return np.hstack([quad, uv]).astype(np.float32)

		def draw_image(image: pygame.Surface, quad: np.ndarray, image_color_mul=(1, 1, 1, 1), image_color_add=(0, 0, 0, 0)):
			quad = gl_scaling(quad)
			quad = attach_uv(quad)
			self.vbo.write(quad)
			self.shader_basic['imageColorMul'].value = image_color_mul
			self.shader_basic['imageColorAdd'].value = image_color_add
			self.textures[image].use()
			self.vao_basic.render()

		# Render Texture Layer
		self.texture_layer_fbo.clear(0.5, 0.9, 0.95, 1)
		self.texture_layer_fbo.use()
		bg_pos = pygame.Vector2(self.rect.topleft)
		bg_pos.x = bg_pos.x // self.bg.get_width() * self.bg.get_width()
		bg_pos.y = bg_pos.y // self.bg.get_height() * self.bg.get_height()
		for i in range(3):
			for j in range(3):
				draw_image(self.bg, rect_to_quad(self.bg.get_rect(topleft=bg_pos + (self.bg.get_width() * i, self.bg.get_height() * j))))
		
		for sprite in ww.group:
			ww.group.change_layer(sprite, sprite.pos.y + isinstance(sprite, Particle) * ww.SCREEN_SIZE.y)
		for sprite in ww.group:
			if isinstance(sprite, DrawableInstance):
				draw_image(sprite.image, sprite.quad, sprite.image_color_mul, sprite.image_color_add)

		# Render Pygame Layer
		self.pg_screen.fill((0, 0, 0, 0))
		for sprite in ww.group:
			if isinstance(sprite, LifeInstance) and not isinstance(sprite, Player):
				hp_rect = sprite.aabb_rect.move(-self.rect.left, -self.rect.top)
				hp_rect = hp_rect.move(0, hp_rect.height + 2)
				hp_rect.height = 4
				pygame.draw.rect(self.pg_screen, (0, 0, 0), hp_rect, 0, 5)
				
				hp_rect = hp_rect.inflate(-2, -2)
				hp_rect.width *= sprite.hp / sprite.mhp
				pygame.draw.rect(self.pg_screen, (255, 0, 0), hp_rect, 0, 5)
			# if isinstance(sprite, DamageNumber):
			# 	text = ww.font12.render(str(round(sprite.num)), False, (0, 0, 0))
			# 	self.pg_screen.blit(text, sprite.pos - (self.rect.left, self.rect.top))
			if hasattr(sprite, 'draw'):
				sprite.draw(self.pg_screen)
		if ww.phase == ww.PHASE.PLAY:
			text = ww.font12.render('밤', False, (255, 255, 255))
			self.pg_screen.blit(text, text.get_rect(midtop=(ww.SCREEN_SIZE[0] / 2, 0)))
			text = ww.font20.render(f'{ww.wave}', False, (255, 255, 255))
			self.pg_screen.blit(text, text.get_rect(midtop=(ww.SCREEN_SIZE[0] / 2, 16)))
			text = ww.font15.render(f'{int((View.NIGHT_LENGTH - self.time) / 60)}', False, (255, 255, 255))
			self.pg_screen.blit(text, text.get_rect(midtop=(ww.SCREEN_SIZE[0] / 2, 36)))

		if ww.DEBUG:
			for sprite in ww.group:
				if isinstance(sprite, CollidableInstance):
					vertices = sprite.vertices - self.rect.topleft
					pygame.draw.polygon(self.pg_screen, (192, 32, 32), vertices, 1)
			self.draw_debug_text()

		self.pg_texture.write(self.pg_screen.get_view('1'))
		self.pg_texture.swizzle = 'BGRA'

		# Render Normal Layer
		self.normal_layer_fbo.clear(0.5, 0.5, 1, 1)
		self.normal_layer_fbo.use()
		for sprite in ww.group:
			if isinstance(sprite, DrawableInstance):
				normal = sprite.normal
				if normal:
					draw_image(normal, sprite.quad)
				else:
					draw_image(sprite.image, sprite.quad, image_color_mul=(0, 0, 0, 1), image_color_add=(0.5, 0.5, 1, 0))
		
		# Lighting
		numLight = 0
		for sprite in ww.group:
			if not isinstance(sprite, BrightInstance) or sprite.light_diffuse == 0:
				continue
			pos = gl_scaling(np.array(sprite.pos))
			self.shader_light[f'light[{numLight}].position'].value = pos[0], -pos[1], 0.1
			self.shader_light[f'light[{numLight}].color'].value = sprite.light_color
			self.shader_light[f'light[{numLight}].diffuse'].value = sprite.light_diffuse, sprite.light_diffuse, sprite.light_diffuse
			self.shader_light[f'light[{numLight}].constant'].value = 1.0
			self.shader_light[f'light[{numLight}].linear'].value = 0.09
			self.shader_light[f'light[{numLight}].quadratic'].value = 0.032

			numLight += 1
			if numLight >= self.MAX_NUM_LIGHT:
				break
		self.shader_light['numLight'].value = numLight
		self.shader_light['flashColor'].value = 1, 1, 1, self.flash
		self.shader_light['ambient'].value = self.ambient

		# UI Layers
		self.ui_layer_fbo.clear(0, 0, 0, 0)
		self.ui_layer_fbo.use()
		if ww.phase == ww.PHASE.PLAY:
			cooltime = [ww.player.m1Attack_time, ww.player.m2Attack_time, ww.player.shift_time, 1]
			for i in range(3):
				rect = pygame.Rect(self.rect.bottomright, (32, 32)).move(-32 * (3 - i), -32).move(-4, -4)
				draw_image(ww.sprites['skill'][i], rect_to_quad(rect))
				rect = pygame.Rect(pygame.Vector2(self.rect.bottomright), (32, 32)).move(-32 * (3 - i), -32).move(-4, -4)
				quad = rect_to_quad(rect)
				quad[0][1] = quad[1][1] = quad[1][1] + 32 * (1 - cooltime[i])
				draw_image(ww.sprites['primitive'][0], quad, image_color_mul=(1, 1, 1, .5 + .5 * (1 - cooltime[i])))
			quad = pygame.Rect((0, 0), (192, 24)).move(0, ww.SCREEN_SIZE[1] - 24).move(self.rect.topleft).move(4, -4)
			quad = rect_to_quad(quad)
			draw_image(ww.sprites['primitive'][0], quad)
			quad = pygame.Rect((0, 0), (192 * ww.player.hp / ww.player.stat.mhp, 24)).move(0, ww.SCREEN_SIZE[1] - 24).move(self.rect.topleft).move(4, -4)
			quad = rect_to_quad(quad)
			draw_image(ww.sprites['primitive'][0], quad, image_color_mul=(0.56, 0.84, 0.47, 1))

		self.pg_post_screen.fill((0, 0, 0, 0))
		if ww.phase == ww.PHASE.PLAY:
			text = ww.font12.render(f'{round(ww.player.hp)} / {round(ww.player.stat.mhp)}', False, (0, 0, 0))
			quad = pygame.Rect((0, 0), (192, 24)).move(0, ww.SCREEN_SIZE[1] - 24).move(4, -4)
			self.pg_post_screen.blit(text, text.get_rect(center=quad.center))
			text_string = ['M1', 'M2', 'Shift', 'R']
			for i in range(3):
				text = ww.font12.render(text_string[i], False, (255, 255, 255))
				rect = pygame.Rect(pygame.Vector2(self.rect.bottomright), (32, 32)).move(-32 * (3 - i), -32).move(-4, -4).move(-self.rect.left, -self.rect.top).move(0, -20)
				self.pg_post_screen.blit(text, text.get_rect(center=rect.center))

			text = ww.font15.render(f'fps: {ww.FPS}', False, (255, 255, 255))
			self.pg_post_screen.blit(text, (10, 10))
			text = ww.font15.render(f'골드: {round(ww.player.gold)}', False, (255, 255, 255))
			self.pg_post_screen.blit(text, (10, 30))

		self.pg_post_texture.write(self.pg_post_screen.get_view('1'))
		self.pg_post_texture.swizzle = 'BGRA'

		# Integrate Layers
		self.ctx.screen.use()
		self.vbo.write(attach_uv(self.screen_quad))

		self.texture_layer.use(location=0)
		self.normal_layer.use(location=1)
		self.vao_light.render()

		self.pg_texture.use()
		self.shader_basic['imageColorMul'].value = 1, 1, 1, 1
		self.shader_basic['imageColorAdd'].value = 0, 0, 0, 0
		self.vao_basic.render()

		self.ui_layer.use()
		self.vao_basic.render()

		self.pg_post_texture.use()
		self.shader_basic['imageColorMul'].value = 1, 1, 1, 1
		self.shader_basic['imageColorAdd'].value = 0, 0, 0, 0
		self.vao_basic.render()