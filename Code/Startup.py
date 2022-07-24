import pygame
import os
import platform 

# Načítanie SDL knižníc
if platform.system() == "Linux":
    os.putenv('SDL_VIDEODRIVER', 'fbcon')
    os.putenv('SDL_FBDEV'      , '/dev/fb0')
    os.putenv('SDL_MOUSEDRV'   , 'TSLIB')

# Inicializácia driverov
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()

from Levels import LevelClass
from AppSettings import GAME


def launch_game():
    # Skrytie kurzora
    pygame.mouse.set_visible(False)

    # Zablokovanie prijímaných eventov 
    pygame.event.set_allowed(None)
    pygame.event.set_allowed(pygame.QUIT)

    GAME.level = LevelClass.Level(1)    # Inicializácia prvej úrovne
    GAME.level.load_assets()            # Načítanie prostriedkov prvej úrovne
    GAME.level.launch_stage()           # Spustenie hlavnej slučky


if __name__ == "__main__":
    launch_game()