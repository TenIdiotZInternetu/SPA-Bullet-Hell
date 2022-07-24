import os, sys
import pygame
from pygame.sprite import DirtySprite, LayeredDirty

from AppSettings import ROOTDIR

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from AppSettings import GAME
from Sprites.Player import PLAYER
from UI.LevelUIComponents import *


class LevelUI():
    def __init__(self):
        self.background = pygame.image.load(str(ROOTDIR/"Assets"/"UI"/"LevelUI.png")).convert_alpha()
        self.image = self.background.copy()

        self.counters = {
            "hp": pygame.sprite.LayeredDirty(),
            "bombs": pygame.sprite.LayeredDirty()
        }
        
        self.score_counter = ScoreCounter(self)
        self.power_gauge = PowerGauge(self)
        self.init_draw()


    def init_draw(self):
        GAME.SCREEN.blit(self.background, (0, 0))
        self.power_gauge.update_power()
        
        x_pos = 532
        y_pos = 123 

        for item, group in self.counters.items():
            for i in range(5):
                group.add(ItemCounter((x_pos, y_pos), item))
                
                if i < getattr(PLAYER, item): group.sprites()[i].visible = 1
                else: group.sprites()[i].visible = 0
                
                x_pos += group.sprites()[0].rect.width + 3

            
            group.draw(self.image)

            x_pos = 532
            y_pos = 202

        rects = self.draw(GAME.SCREEN)
        pygame.display.update(rects)


    def draw(self, surface):
        return surface.blit(self.image, (0,0))


    def draw_UI_element(self, element):
        element.dirty = 1
        element.group.draw(self.image)
        element.group.clear(self.image, self.background)


    def update_item_count(self, item_type):
        items = self.counters[item_type].sprites()
        item_count = getattr(PLAYER, item_type)
        self.counters[item_type].clear(self.image, self.background)

        for i in range(5):
            if i < item_count: items[i].visible = True
            else: items[i].visible = False

            items[i].dirty = 1
            
        self.counters[item_type].draw(self.image)
        rects = self.draw(GAME.SCREEN)
        pygame.display.update(rects)












