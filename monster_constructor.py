import pygame
import globals
from monster import *
import random

class MonsterConstuctor:
    def __init__(self):
        super().__init__()
        self.monster_list = ['Tree']
        self.pos = globals.view.rect.center
        self.construtor_time = 0
        self.construtor_delay = 60

    def update(self):
        if self.construtor_time == self.construtor_delay:
            globals.tree_group.add(Tree((0,0)))
            globals.group.add(globals.tree_group)
            self.construtor_time = 0
        self.construtor_time += 1
