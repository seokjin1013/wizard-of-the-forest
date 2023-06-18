from instance import *
import ww
import pygame
import item
import random

# managing shop GUI button placement and buying process
class Shop(Instance):
    def __init__(self, pos):
        super().__init__(pos)

        # draw many of buttons

        def draw(self, surface):
            text = ww.font20.render(f'{ww.wave}일 째', False, (0, 0, 0))
            text_rect = text.get_rect(center=self.rect.center)
            surface.blit(text, text_rect)
        item_button = ShopButton(pygame.Rect(10, 320, 90, 30), None, draw)
        ww.group.add(item_button)

        def draw(self, surface):
            surface.blit(ww.sprites['icons'][0], ww.sprites['icons'][0].get_rect(midleft=pygame.Vector2(self.rect.midleft) + (5, 0)))
            text = ww.font20.render(f'{int(ww.player.gold):d}', False, (0, 0, 0))
            text_rect = text.get_rect(midright=pygame.Vector2(self.rect.midright) - (5, 0))
            surface.blit(text, text_rect)
        item_button = ShopButton(pygame.Rect(110, 320, 100, 30), None, draw)
        ww.group.add(item_button)

        def draw(self, surface):
            surface.blit(ww.sprites['icons'][1], ww.sprites['icons'][1].get_rect(midleft=pygame.Vector2(self.rect.midleft) + (5, 0)))
            text = ww.font20.render(f'{ww.player.skill_point}', False, (0, 0, 0))
            text_rect = text.get_rect(midright=pygame.Vector2(self.rect.midright) - (5, 0))
            surface.blit(text, text_rect)
        item_button = ShopButton(pygame.Rect(220, 320, 100, 30), None, draw)
        ww.group.add(item_button)

        def draw(self, surface):
            text = ww.font20.render('아이템', False, (0, 0, 0))
            text_rect = text.get_rect(center=self.rect.center)
            surface.blit(text, text_rect)
        def callback(s):
            self.phase_set(0)
        item_button = ShopButton(pygame.Rect(10, 10, 80, 30), callback, draw)
        ww.group.add(item_button)

        def draw(self, surface):
            text = ww.font20.render('스킬강화', False, (0, 0, 0))
            text_rect = text.get_rect(center=self.rect.center)
            surface.blit(text, text_rect)
        def callback(s):
            self.phase_set(1)
        item_button = ShopButton(pygame.Rect(100, 10, 80, 30), callback, draw)
        ww.group.add(item_button)

        def draw(self, surface):
            text = ww.font15.render(f'기본효과', False, (0, 0, 0))
            text_rect = text.get_rect(topleft=pygame.Vector2(self.rect.topleft) + (10, 10))
            surface.blit(text, text_rect)
            text = [
                f'공격력: {ww.player.stat.atk:.2f}',
                f'공격속도: {ww.player.stat.atk_firerate:.2f}',
                f'이동속도: {ww.player.stat.speed:.2f}',
                f'최대체력: {ww.player.stat.mhp:.2f}',
                f'투사체 속도: {ww.player.stat.atk_velocity:.2f}',
                f'투사체 체공시간: {ww.player.stat.atk_duration:.2f}',
                f'치명타 계수: {ww.player.stat.crit_atk:.2f}',
                f'치명타 확률: {ww.player.stat.crit:.2f}',
                f'골드 획득 계수: {ww.player.stat.gold_earn:.2f}',
            ]
            for i, t in enumerate(text):
                t = ww.font12.render(t, False, (0, 0, 0))
                text_rect = t.get_rect(topleft=pygame.Vector2(self.rect.topleft) + (10, 10) + (0, 20 * (i + 1)))
                surface.blit(t, text_rect)
            
        # buying items
        item_button = ShopButton(pygame.Rect(460, 10, 170, 300), None, draw)
        ww.group.add(item_button)

        def draw(self, surface):
            text = ww.font20.render(f'다음으로', False, (0, 0, 0))
            text_rect = text.get_rect(center=self.rect.center)
            surface.blit(text, text_rect)
        def callback(s):
            ww.phase = ww.PHASE.PLAY
            ww.wave += 1
            ww.player.skill_point += 1
        item_button = ShopButton(pygame.Rect(460, 320, 170, 30), callback, draw)
        ww.group.add(item_button)

        self.phase_button = [
            set(), set()
        ]

        self.reroll_cnt = 0
        self.reroll_item()

        # buying skill
        skill_name = ['기본공격', '강공격', '이동기']
        for i in range(3):
            def make_draw(i):
                def draw(self, surface):
                    skill_info = [
                        [f'추가공격력+{ww.player.skill_level[0] * 5}%'],
                        [f'추가공격력+{(ww.player.skill_level[1] + 1) // 2 * 20}%', f'쿨타임-{(ww.player.skill_level[1]) // 2 * 0.5}'],
                        [f'쿨타임-{ww.player.skill_level[2] * 0.7}']
                    ]
                    text = ww.font20.render(f'{skill_name[i]}', False, (0, 0, 0))
                    text_rect = text.get_rect(center=pygame.Vector2(self.rect.center) - (0, 90))
                    surface.blit(text, text_rect)
                    img = ww.sprites['skill'][i]
                    img = pygame.transform.scale2x(img)
                    surface.blit(img, img.get_rect(center=self.pos - (0, 60)))
                    text = ww.font15.render(f'효과', False, (0, 0, 0))
                    text_rect = text.get_rect(center=pygame.Vector2(self.rect.center) - (0, 30))
                    surface.blit(text, text_rect)
                    for j, info in enumerate(skill_info[i]):
                        text = ww.font15.render(f'{info}', False, (0, 0, 0))
                        text_rect = text.get_rect(center=pygame.Vector2(self.rect.center) - (0, 0 - 15 * j))
                        surface.blit(text, text_rect)
                return draw
            item_button = ShopButton(pygame.Rect(10 + (420 / 3 + 10) * i, 50, 420 / 3, 220), None, make_draw(i))
            self.phase_button[1].add(item_button)
            

            def make_draw():
                def draw(self, surface):
                    text = ww.font20.render(f'강화 1', False, (0, 0, 0))
                    text_rect = text.get_rect(center=pygame.Vector2(self.rect.center))
                    surface.blit(text, text_rect)
                return draw

            def make_callback(i):
                def callback(s):
                    if ww.player.skill_point >= 1:
                        # item_button.kill()
                        # s.kill()
                        # self.phase_button[0].discard(item_button)
                        # self.phase_button[0].discard(s)
                        ww.player.skill_point -= 1
                        ww.player.skill_level[i] += 1
                        # ww.player.apply_item()
                return callback
            
            item_button = ShopButton(pygame.Rect(10 + (420 / 3 + 10) * i, 280, 420 / 3, 30), make_callback(i), make_draw())
            self.phase_button[1].add(item_button)

        self.phase_set(0)


    def phase_set(self, phase):
        self.phase = phase
        for group in self.phase_button:
            for sprite in group:
                sprite.kill()
        for sprite in self.phase_button[phase]:
            ww.group.add(sprite)


    # reroll items usecase
    def reroll_item(self):
        self.phase_button[0].clear()
        random_numbers = np.random.choice(len(item.items_tier3_name), 4, replace=False)
        items = [item.ItemTier3(number) for number in random_numbers]
        def draw(s, surface):
            cost = 1 + ww.player.reroll_cnt * (ww.player.reroll_cnt // 6)
            text = ww.font20.render(f'새로고침 {cost}', False, (0, 0, 0))
            text_rect = text.get_rect(center=s.rect.center)
            surface.blit(text, text_rect)
        def callback(s):
            cost = 1 + ww.player.reroll_cnt * (ww.player.reroll_cnt // 6)
            if ww.player.gold >= cost:
                ww.player.gold -= cost
                ww.player.reroll_cnt += 1
                for group in self.phase_button:
                    for sprite in group:
                        sprite.kill()
                self.reroll_item()
                self.phase_set(0)
        item_button = ShopButton(pygame.Rect(340, 10, 110, 30), callback, draw)
        self.phase_button[0].add(item_button)

        for i in range(4):
            def make_draw(i):
                def draw(self, surface):
                    text = ww.font20.render(f'티어{items[i].tier}', False, (0, 0, 0))
                    text_rect = text.get_rect(center=pygame.Vector2(self.rect.center) - (0, 90))
                    surface.blit(text, text_rect)
                    surface.blit(items[i].image, items[i].rect(center=self.pos - (0, 60)))
                    text = ww.font15.render(f'{items[i].name}', False, (0, 0, 0))
                    text_rect = text.get_rect(center=pygame.Vector2(self.rect.center) - (0, 30))
                    surface.blit(text, text_rect)
                    for j, info in enumerate(items[i].info):
                        text = ww.font15.render(f'{info}', False, (0, 0, 0))
                        text_rect = text.get_rect(center=pygame.Vector2(self.rect.center) - (0, 0 - 15 * j))
                        surface.blit(text, text_rect)
                return draw
            item_button = ShopButton(pygame.Rect(10 + (410 / 4 + 10) * i, 50, 410 / 4, 220), None, make_draw(i))
            self.phase_button[0].add(item_button)
            
            cost = 0
            if items[i].tier == 3:
                cost = 25 + random.randint(-7, 7) + ww.wave
            if items[i].tier == 2:
                cost = 60 + random.randint(-15, 15) + ww.wave * 1.5
            if items[i].tier == 1:
                cost = 100 + random.randint(-22, 22) + ww.wave * 2
            if items[i].tier == 0:
                cost = 120 + ww.wave * 3
            cost = round(cost)

            def make_draw(cost):
                def draw(self, surface):
                    text = ww.font20.render(f'구매 {cost}', False, (0, 0, 0))
                    text_rect = text.get_rect(center=pygame.Vector2(self.rect.center))
                    surface.blit(text, text_rect)
                return draw

            def make_callback(item_button, cost, i):
                def callback(s):
                    if ww.player.gold >= cost:
                        item_button.kill()
                        s.kill()
                        self.phase_button[0].discard(item_button)
                        self.phase_button[0].discard(s)
                        ww.player.gold -= cost
                        ww.player.items_tier3[i] += 1
                        ww.player.apply_item()
                return callback
            
            item_button = ShopButton(pygame.Rect(10 + (410 / 4 + 10) * i, 280, 410 / 4, 30), make_callback(item_button, cost, random_numbers[i]), make_draw(cost))
            self.phase_button[0].add(item_button)


# check mouse position and mouse extends, click recognization
class ShopButton(Instance):
    def __init__(self, rect, callback, draw):
        super().__init__(rect.center)
        self.rect = rect
        self.callback = callback
        self.draw_sub = draw

    def update(self):
        if ww.controller.mouse_left_pressed:
            if self.rect.move(ww.view.rect.topleft).collidepoint(ww.controller.mouse_pos):
                if self.callback:
                    pygame.mixer.find_channel(True).play(ww.sounds['text'])
                    self.callback(self)
        if ww.phase != ww.PHASE.SHOP:
            self.kill()
        super().update()

    def draw(self, surface):
        pygame.draw.rect(surface, pygame.Color(255, 255, 255, 192), self.rect)
        self.draw_sub(self, surface)