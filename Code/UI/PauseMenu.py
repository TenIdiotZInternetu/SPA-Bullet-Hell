import os, sys
import pygame
from pygame.constants import SRCALPHA
from pygame.sprite import DirtySprite, LayeredDirty

from UserInput import USERINPUT

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from AppSettings import GAME, ROOTDIR


class PauseMenuBG(DirtySprite):
    def __init__(self):
        DirtySprite.__init__(self)
        self.image = pygame.Surface((800, 480), flags = SRCALPHA)
        self.image.fill((0, 0, 0, 128))
        self.rect = self.image.get_rect()

        self.visible = 0


class PauseMenu():
    pfont = pygame.font.Font(str(ROOTDIR/"Assets"/"Fonts"/"revuebt.ttf"), 72)
    bg = PauseMenuBG()


    def show():
        GAME.SCREEN.fill((0, 0, 0, 10))
        pause_header = PauseMenu.pfont.render("PAUSED", True, "#FFFFFF")

        PauseMenu.bg.blit(GAME.SCREEN, (0, 0))
        pause_header.blit(GAME.SCREEN, (300, 200))

        pygame.display.flip()

        while USERINPUT.BUTTON_START: pass
        PauseMenu.update()


    def update():
        while GAME.level.is_paused: 
            USERINPUT.update()
            if USERINPUT.BUTTON_START: GAME.level.is_paused = False

            



