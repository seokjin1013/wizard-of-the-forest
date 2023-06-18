import pygame
import ww
from monster import *
import moderngl
import numpy as np

class View:
	MAX_NUM_LIGHT = 60
	def __init__(self, target=None):
		self.rect = pygame.Rect((0, 0), ww.SCREEN_SIZE)
		self.target = target
		self.bg = ww.backgrounds['stage1']
		self.screen_quad = np.array([[-1, 1], [1, 1], [1, -1], [-1, -1]])
		self.font = pygame.font.SysFont("Verdana", 20)
		self.debug_text = []

		self.ctx = moderngl.create_context()
		self.ctx.enable_only(moderngl.BLEND)
		self.program = self.ctx.program(
			vertex_shader="""
				#version 330
				layout (location = 0) in vec2 in_uv;
				layout (location = 1) in vec2 in_position;
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
				in vec2 v_uv;
				void main() 
				{
					fragColor = texture(u_texture, v_uv);
				}
			"""
		)
		self.program2 = self.ctx.program(
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
				
					vec3 ambient;
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

				vec3 CalcPointLight(Light light, vec3 normal, vec3 fragPos)
				{
					vec3 lightDir = normalize(light.position - fragPos);
					
					float diff = max(dot(normal, lightDir), 0.0);
					
					float distance    = length(light.position - fragPos);
					float attenuation = 1.0 / (light.constant + light.linear * distance + 
								light.quadratic * (distance * distance));    
					
					vec3 ambient  = light.ambient  * texture(u_texture, v_uv).rgb;
					vec3 diffuse  = light.diffuse  * diff * texture(u_texture, v_uv).rgb;
					ambient  *= attenuation;
					diffuse  *= attenuation;
					return (ambient + diffuse);
				}

				void main() 
				{
					vec3 lightColor = vec3(1, 1, 1);
					vec3 objectColor = texture(u_texture, v_uv).rgb;

					vec3 norm = normalize(texture(u_normal, v_uv).xyz - vec3(0.5, 0.5, 0.5));
					norm.x = -norm.x;
					vec3 result = vec3(0, 0, 0);
					for(int i = 0; i < numLight; i++)
						result += CalcPointLight(light[i], norm, vec3(fragPos.xy, 0.0));
					fragColor = vec4(result, 1.0);
				}
			""" % View.MAX_NUM_LIGHT
		)
		self.program2['u_texture'] = 0
		self.program2['u_normal'] = 1

		self.vbo = self.ctx.buffer(None, reserve=4 * 4 * 4)
		self.vao = self.ctx.vertex_array(self.program, [(self.vbo, "2f4 2f4", "in_position", "in_uv")])
		
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
			self.textures[image] = texture

		self.pg_screen = pygame.Surface(self.rect.size, flags=pygame.SRCALPHA)
		self.pg_texture = self.ctx.texture(self.rect.size, 4)
		self.pg_texture.filter = moderngl.NEAREST, moderngl.NEAREST

		self.texture_layer = self.ctx.texture(self.rect.size, 4)
		self.texture_layer.filter = moderngl.NEAREST, moderngl.NEAREST
		self.texture_layer_fbo = self.ctx.framebuffer(self.texture_layer)
		self.normal_layer = self.ctx.texture(self.rect.size, 4)
		self.normal_layer.filter = moderngl.NEAREST, moderngl.NEAREST
		self.normal_layer_fbo = self.ctx.framebuffer(self.normal_layer)
		self.vao2 = self.ctx.vertex_array(self.program2, [(self.vbo, "2f4 2f4", "in_position", "in_uv")])

	def update(self):
		if self.target:
			self.rect.center = self.target.pos

	def draw_debug_text(self):
		for idx, text in enumerate(self.debug_text):
			text = self.font.render(str(text), True, (0, 0, 0))
			self.pg_screen.blit(text, (10, 10 + idx * 20))
		self.debug_text.clear()

	def draw(self):
		def get_quad(rect):
			return np.array([rect.topleft, rect.topright, rect.bottomright, rect.bottomleft])

		def gl_scaling(quad):
			quad = (quad - self.rect.topleft) / ww.SCREEN_SIZE * 2 - 1
			return quad
		
		def attach_uv(quad):
			uv = np.array([
				[0, 0], [1, 0], [1, 1], [0, 1],
			])
			return np.hstack([quad, uv]).astype(np.float32)

		def draw_texture(quad, texture):
			if isinstance(quad, pygame.rect.Rect):
				quad = get_quad(quad)
			quad = gl_scaling(quad)
			quad = attach_uv(quad)
			self.vbo.write(quad)
			texture.use()
			self.vao.render(moderngl.TRIANGLE_FAN)

		# Render Texture Layer
		self.texture_layer_fbo.clear(0.5, 0.9, 0.95, 1)
		self.texture_layer_fbo.use()
		draw_texture(self.bg.get_rect(), self.textures[self.bg])
		
		for sprite in ww.group:
			ww.group.change_layer(sprite, sprite.pos.y)
		for sprite in ww.group:
			draw_texture(sprite.get_quad(), self.textures[sprite.get_image()])

		# Render Pygame Layer
		self.pg_screen.fill((0, 0, 0, 0))
		for sprite in ww.group:
			if isinstance(sprite, Tree):
				hp_rect = sprite.get_aabb_rect().move(-self.rect.left, -self.rect.top)
				hp_rect = hp_rect.move(0, hp_rect.height + 2)
				hp_rect.height = 4
				pygame.draw.rect(self.pg_screen, (0, 0, 0), hp_rect, 0, 5)
				
				hp_rect = hp_rect.inflate(-2, -2)
				hp_rect.width *= sprite.hp / sprite.mhp
				pygame.draw.rect(self.pg_screen, (255, 0, 0), hp_rect, 0, 5)

		if ww.DEBUG:
			for sprite in ww.group:
				vertices = sprite.get_vertices() - self.rect.topleft
				pygame.draw.polygon(self.pg_screen, (192, 32, 32), vertices, 1)
			self.draw_debug_text()

		self.pg_texture.write(self.pg_screen.get_view('1'))
		self.pg_texture.swizzle = 'BGRA'

		# Render Normal Layer
		self.normal_layer_fbo.clear(0.5, 0.5, 1, 1)
		self.normal_layer_fbo.use()
		for sprite in ww.group:
			normal = sprite.get_normali()
			if normal:
				draw_texture(sprite.get_quad(), self.textures[normal])
		
		# Lighting
		numLight = 0
		for sprite in ww.group:
			if sprite.light_diffuse == 0:
				continue
			pos = gl_scaling(np.array(sprite.pos))
			self.program2[f'light[{numLight}].position'].value = pos[0], -pos[1], 0.1
			self.program2[f'light[{numLight}].ambient'].value = sprite.light_ambient, sprite.light_ambient, sprite.light_ambient
			self.program2[f'light[{numLight}].diffuse'].value = sprite.light_diffuse, sprite.light_diffuse, sprite.light_diffuse
			self.program2[f'light[{numLight}].constant'].value = 1.0
			self.program2[f'light[{numLight}].linear'].value = 0.09
			self.program2[f'light[{numLight}].quadratic'].value = 0.032

			numLight += 1
			if numLight >= self.MAX_NUM_LIGHT:
				break
		self.program2['numLight'].value = numLight

		# Integrate Layers
		self.ctx.screen.use()
		self.vbo.write(attach_uv(self.screen_quad))

		self.texture_layer.use(location=0)
		self.normal_layer.use(location=1)
		self.vao2.render(moderngl.TRIANGLE_FAN)

		self.pg_texture.use()
		self.vao.render(moderngl.TRIANGLE_FAN)