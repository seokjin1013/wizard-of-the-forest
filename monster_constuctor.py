import pygame
import ww
from monster import *
import random

class MonsterConstuctor:
    def __init__(self):
        super().__init__()
        self.monster_list = ['Tree']
        self.pos = ww.view.rect.center
        self.construtor_time = 0
        self.construtor_delay = 60

    def update(self):
        if self.construtor_time == self.construtor_delay:
            ww.tree_group.add(Tree((0,0)))
            ww.group.add(ww.tree_group)
            self.construtor_time = 0
        self.construtor_time += 1
