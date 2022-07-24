import pygame
import os, sys, pathlib
from pygame import DOUBLEBUF, HWSURFACE

# Pripnutie adresy súboru ku koreňovej adrese projektu
currentdir = os.path.dirname(os.path.realpath(__file__)) 
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)


class Game():
    def __init__(self):
        self.SCREEN_WIDTH = 800     	     # šírka obrazovky
        self.SCREEN_HEIGHT = 480             # výška obrazovky
        self.FPS = 60
        self.CLOCK = pygame.time.Clock()     # objekt časovača
        flags = DOUBLEBUF | HWSURFACE        # vlastnosti vykreslovania okna pre väčśi výkon

        # inicializácia okna s rozmermi obrazovky
        self.SCREEN = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        self.level = None
        
    
    

# Globálne premenné
GAME = Game()
ROOTDIR = pathlib.Path(__file__).parent.parent # Koreňová adresa aplikácie