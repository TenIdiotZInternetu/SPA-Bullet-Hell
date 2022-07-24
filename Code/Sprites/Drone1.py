import os, sys, pathlib
import pygame
import math

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

filepath = pathlib.Path(__file__).parent

from AppSettings import GAME
from Sprites.Enemy import EnemySprite
from Sprites.BulletTypes import *
from Sprites.Powerups import *
import MovementPatterns as MP
from Vectors import VectorPlus
from AppSettings import ROOTDIR


class Drone1(EnemySprite):
    def __init__(self):
        super().__init__()
        self.image_clean = pygame.transform.flip(pygame.image.load(
            str(ROOTDIR/'Assets'/'Ships'/ "Drone1.png")).convert_alpha(), False, True)
        self.image = self.image_clean.copy()
        self.mask = pygame.mask.from_surface(self.image, 1)

        self.set_defaults()

    # Nastaví východzie vlastnosti, prevažne a zdravie a časovače 
    def set_defaults(self):
        self.super_defaults()
        
        self.hp = 6
        self.shot_timer = 28

    # Aktualizácia časovačov, pokyny pre streľbu,
    # ďaľšie funkcionality špecifické pre konkrétny typ nepriateľa 
    def update(self):
        self.super_update()
        
        self.shot_timer -= 1
        
        if self.shot_timer == 0:
            self.shoot()
            self.shot_timer = 40
        
    # Pridanie projektilov do groups,
    # umiestnenie na pozíciu dela
    def shoot(self):
        bullet = GAME.level.queues[BulletBasic].get()

        bullet.spawn((self.rect.centerx + self.turret_pos.x,
                      self.rect.centery + self.turret_pos.y))

        bullet.rotate(self.rotation)
        bullet.movement_pattern.change_angle(self.rotation)

    # Zavolá super_spawn(), nastaví vzor pohybu
    def spawn(self, position, mp):
        self.super_spawn(position)
        self.movement_pattern = mp
        mp.init_vector()

    # Chovanie objekty pri dosiahnutí 0 zdravia
    # Pridá hráčovi skóre, vypustí vylepšenia lode,
    # odstráni objekt z groups apod.
    def die(self):
        GAME.level.UI.score_counter.update_score(400)

        powerup = GAME.level.queues[Powerup].get()
        powerup.spawn(self.rect.center)

        self.despawn()

    # Nastaví pozíciu diel
    def set_turret_positions(self):
        self.turret_pos = VectorPlus.from_angle(self.rotation) * (self.rect.height / 2 + 3)
        

