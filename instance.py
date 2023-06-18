import pygame
import ww
import Box2D

class Instance(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        pos = Box2D.b2Vec2(pos)
        self.image = ww.images[self.__class__]
        self.body = ww.world.CreateDynamicBody(position=pos / ww.PPM)
        self.body.CreateFixture(ww.fixture_defs[self.__class__])
        self.body.fixedRotation = True
        self.body.userData = self
        self.pos = pos
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        self.pos = self.body.transform.position * ww.PPM
    
    def kill(self):
        ww.world.DestroyBody(self.body)
        super().kill()