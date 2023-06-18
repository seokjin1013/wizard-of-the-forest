from instance import DrawableInstance
import ww
import controller
import pygame

# the title in first of game
class Title(DrawableInstance):
    def __init__(self, pos):
        super().__init__(pos)
        self.sprite_index = ww.sprites['title']

    def update(self):
        if ww.phase != ww.PHASE.TITLE:
            self.kill()

# start button or exit button
class TitleButton(DrawableInstance):
    def __init__(self, pos, idx, callback=None):
        super().__init__(pos)
        self.sprite_index = ww.sprites['title_buttons']
        self.image_speed = 0
        self.image_index = idx
        self.callback = callback

    def update(self):
        if ww.controller.mouse_left_down:
            if self.image.get_rect(center=self.pos).collidepoint(ww.controller.mouse_pos):
                if self.callback:
                    self.callback()
        if ww.phase != ww.PHASE.TITLE:
            self.kill()
        super().update()
