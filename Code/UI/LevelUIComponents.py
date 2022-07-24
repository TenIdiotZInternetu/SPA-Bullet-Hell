import os, sys
import pygame
from pygame.sprite import DirtySprite, LayeredDirty

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from AppSettings import GAME, ROOTDIR
from Sprites.Player import PLAYER


class ForegroundElement(DirtySprite):
    def __init__(self, image_path, pos, parentUI=None):
        DirtySprite.__init__(self)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.parentUI = parentUI

        self.group = LayeredDirty(self)


class ItemCounter(DirtySprite):
    def __init__(self, pos, item_type):
        DirtySprite.__init__(self)
        self.hp_img = pygame.image.load(str(ROOTDIR/"Assets"/"Placeholders"/"hp_indicator.png")).convert_alpha()
        self.bombs_img = pygame.image.load(str(ROOTDIR/"Assets"/"Placeholders"/"hp_indicator.png")).convert_alpha()

        self.image = eval("self." + item_type + "_img.copy()")
        self.rect = self.image.get_rect(topleft = pos)


class GaugeFilling(DirtySprite):
    def __init__(self, bottom_y, left, parentUI):
        DirtySprite.__init__(self)
        self.image = pygame.Surface((4, 1))
        self.rect = self.image.get_rect()
        self.bottom_y = bottom_y
        self.left = left

        self.bottom_row = pygame.Rect(self.left, self.bottom_y - 1, 4, 15)

        self.parentUI = parentUI
        self.group = LayeredDirty(self)


    def update(self, value):
        #if value % 1 == 0: self.image = pygame.transform.scale(self.image, (4, value))
        self.rect = self.image.get_rect(top = self.bottom_y, left = self.left)
        self.rect.top = self.bottom_y - value

        self.image.fill((78, 252, 81))
        
        self.parentUI.draw_UI_element(self)


class ScoreCounter(DirtySprite):
    def __init__(self, parent):
        DirtySprite.__init__(self)
        self.parentUI = parent
        self.font = pygame.font.Font(str(ROOTDIR/"Assets"/"Fonts"/"revuebt.ttf"), 38)

        self.frame = ForegroundElement(str(ROOTDIR/"Assets"/"UI"/"ScoreGauge.png"), (10, 20))
        self.gauge = GaugeFilling(447, 12, self.parentUI)

        self.score = 0
        self.score_string = "{:0>8}".format(self.score)

        self.image = self.font.render(self.score_string, True, (255, 255, 255))
        self.rect = self.image.get_rect(top=36 , left=540)

        self.group = LayeredDirty(self, self.gauge, self.frame)
        self.parentUI.draw_UI_element(self)


    def update_score(self, value):
        self.score += value
        self.score = max(self.score, 0)
        
        self.score_string = "{:0>8}".format(self.score)
        self.image = self.font.render(self.score_string, True, (255, 255, 255))

        gauge_value = 410 / 1000000 * (self.score % 1000000)

        self.gauge.update(gauge_value)
        self.parentUI.draw_UI_element(self)
        self.parentUI.draw_UI_element(self.frame)


class PowerGauge(DirtySprite):
    def __init__(self, parent):
        DirtySprite.__init__(self)
        self.parentUI = parent
        self.font = pygame.font.Font(str(ROOTDIR/"Assets"/"Fonts"/"revuebt.ttf"), 14)

        self.frame = ForegroundElement(str(ROOTDIR/"Assets"/"UI"/"PowerGauge.png"), (514, 243))
        self.gauge = GaugeFilling(458, 516, self.parentUI)

        self.value_string = "{} / 200".format(PLAYER.power_level)

        self.image = self.font.render(self.value_string, True, (255, 255, 255))
        self.rect = self.image.get_rect(left=527, centery = 458)

        self.group = LayeredDirty(self, self.gauge, self.frame)
        self.group.change_layer(self.group.sprites()[-1], 10)
        self.parentUI.draw_UI_element(self)

    
    def update_power(self):
        self.value_string = "< {} / 200".format(PLAYER.power_level)
        self.image = self.font.render(self.value_string, True, (255, 255, 255))

        self.gauge.update(PLAYER.power_level)
        self.parentUI.draw_UI_element(self)

        self.rect.centery = 455 - PLAYER.power_level