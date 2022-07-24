from pygame.sprite import Sprite
from AppSettings import Game
import os, sys
import pygame

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from AppSettings import GAME


class Playfield(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = pygame.Surface((482, 445)).convert()
        self.rect = self.image.get_rect(top = 17, left = 25)
        
        self.bg = self.image.copy()
        self.bg.fill((0, 0, 0))


    def draw(self):
        return GAME.SCREEN.blit(self.image, self.rect)