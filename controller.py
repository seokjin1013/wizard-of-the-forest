import pygame
import ww

class Controller:
    def __init__(self):
        self._left = [pygame.K_a, pygame.K_LEFT]
        self._right = [pygame.K_d, pygame.K_RIGHT]
        self._up = [pygame.K_w, pygame.K_UP]
        self._down = [pygame.K_s, pygame.K_DOWN]
        self._shift = [pygame.K_LSHIFT, pygame.K_RSHIFT]
        self._keys = None
        self._prev_mouses = None
        self._mouses = None

    def update(self):
        self._keys = pygame.key.get_pressed()
        self._prev_mouses = self._mouses
        self._mouses = pygame.mouse.get_pressed()
    
    @property
    def left(self):
        for k in self._left:
            if self._keys[k]:
                return True
        return False

    @property
    def right(self):
        for k in self._right:
            if self._keys[k]:
                return True
        return False

    @property
    def up(self):
        for k in self._up:
            if self._keys[k]:
                return True
        return False

    @property
    def down(self):
        for k in self._down:
            if self._keys[k]:
                return True
        return False
    
    @property
    def shift(self):
        for k in self._shift:
            if self._keys[k]:
                return True
        return False

    @property
    def horizontal(self):
        return self.right - self.left

    @property
    def vertical(self):
        return self.down - self.up

    @property
    def direction(self):
        dir = pygame.Vector2(self.horizontal, self.vertical)
        if not dir:
            return dir
        return dir.normalize()

    @property
    def mouse_left_pressed(self):
        return self._mouses[0] and not self._prev_mouses[0]

    @property
    def mouse_left_down(self):
        return self._mouses[0]

    @property
    def mouse_right_pressed(self):
        return self._mouses[2] and not self._prev_mouses[2]

    @property
    def mouse_right_down(self):
        return self._mouses[2]

    @property
    def mouse_pos(self):
        return pygame.Vector2(pygame.mouse.get_pos()) / (ww.WINDOW_SIZE.x / ww.SCREEN_SIZE.x) + ww.view.rect.topleft