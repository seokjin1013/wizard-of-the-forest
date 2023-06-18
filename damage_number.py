from instance import TemporaryInstance
import ww
class DamageNumber(TemporaryInstance):
    def __init__(self, pos, num, crit):
        super().__init__(pos)
        self.num = num
        self.crit = crit
        self.dur = crit * 50 + 30
    
    def update(self):
        super().update()

    def draw(self, screen):
        color = (160, 100, 0) if not self.crit else (160, 30, 0)
        font = ww.font12 if not self.crit else ww.font15
        text = font.render(str(round(self.num)), False, color)
        rect = text.get_rect(center=self.pos).move(-ww.view.rect.left, -ww.view.rect.top)
        screen.blit(text, rect)